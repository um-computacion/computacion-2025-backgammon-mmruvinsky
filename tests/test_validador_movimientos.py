from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos
from source.validador_movimientos import ValidadorMovimientos
import unittest

class TestValidadorMovimientos(unittest.TestCase):
    """
    Tests para ValidadorMovimientos.
    
    Cobertura:
    - Validación de origen con fichas propias
    - Validación de destino bloqueado
    - Validación de bear-off
    - Validación de entrada desde barra
    - Cálculo de índice de entrada
    """
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.__tablero__ = Tablero()
        self.__gestor_turnos__ = GestorTurnos()
        self.__validador__ = ValidadorMovimientos(self.__tablero__, self.__gestor_turnos__)
    
    def test_validar_movimiento_origen_valido(self):
        """Test: Movimiento desde origen válido debe ser aceptado"""
        # Posición 0 tiene 2 blancas en setup inicial
        es_valido, mensaje = self.__validador__.validar_movimiento(0, 3)
        # Destino 3 está vacío, debe ser válido
        self.assertTrue(es_valido)
        self.assertEqual(mensaje, "")
    
    def test_validar_movimiento_origen_sin_fichas(self):
        """Test: Movimiento desde posición sin fichas propias debe fallar"""
        # Posición 1 está vacía en setup inicial
        es_valido, mensaje = self.__validador__.validar_movimiento(1, 3)
        self.assertFalse(es_valido)
        self.assertIn("origen", mensaje.lower())
    
    def test_validar_movimiento_origen_con_fichas_rivales(self):
        """Test: Movimiento desde posición con fichas rivales debe fallar"""
        # Posición 23 tiene fichas negras
        es_valido, mensaje = self.__validador__.validar_movimiento(23, 3)
        self.assertFalse(es_valido)
        self.assertIn("origen", mensaje.lower())
    
    def test_validar_movimiento_destino_bloqueado(self):
        """Test: Movimiento a destino bloqueado (2+ fichas rivales) debe fallar"""
        # Crear situación con destino bloqueado
        # Posición 5 tiene -5 fichas negras en setup inicial
        es_valido, mensaje = self.__validador__.validar_movimiento(0, 5)
        self.assertFalse(es_valido)
        self.assertIn("bloqueada", mensaje.lower())
    
    def test_validar_movimiento_destino_con_blot_rival(self):
        """Test: Movimiento a destino con 1 ficha rival debe ser válido (captura)"""
        # Configurar tablero manualmente para test
        posiciones = self.__tablero__._obtener_posiciones_ref()
        posiciones[3] = -1  # Colocar 1 ficha negra en posición 3
        
        # Mover blanca de 0 a 3
        es_valido, mensaje = self.__validador__.validar_movimiento(0, 3)
        self.assertTrue(es_valido)
    
    def test_validar_bear_off_sin_fichas_en_home(self):
        """Test: Bear-off sin todas las fichas en home debe fallar"""
        # En setup inicial no todas están en home
        # Intentar bear-off desde posición 18 (home de blancas)
        es_valido, mensaje = self.__validador__.validar_movimiento(18, 6)
        self.assertFalse(es_valido)
        self.assertIn("home", mensaje.lower())
    
    def test_validar_bear_off_con_todas_en_home(self):
        """Test: Bear-off con todas en home y distancia correcta debe ser válido"""
        # Configurar todas las blancas en home (18-23)
        posiciones = self.__tablero__._obtener_posiciones_ref()
        # Limpiar tablero
        for i in range(24):
            posiciones[i] = 0
        # Colocar todas las blancas en home
        posiciones[18] = 5
        posiciones[19] = 5
        posiciones[20] = 5
        
        # Bear-off desde 20 con dado 4 (necesita 24-20=4)
        es_valido, mensaje = self.__validador__.validar_movimiento(20, 4)
        self.assertTrue(es_valido)
    
    def test_validar_bear_off_overshoot_sin_fichas_adelantadas(self):
        """Test: Bear-off con overshoot sin fichas adelantadas debe ser válido"""
        # Configurar escenario
        posiciones = self.__tablero__._obtener_posiciones_ref()
        for i in range(24):
            posiciones[i] = 0
        posiciones[22] = 2  # Solo fichas en 22
        
        # Bear-off desde 22 con dado 6 (necesita 2, sobra 4)
        es_valido, mensaje = self.__validador__.validar_movimiento(22, 6)
        self.assertTrue(es_valido)
    
    def test_validar_bear_off_overshoot_con_fichas_adelantadas(self):
        """Test: Bear-off con overshoot y fichas adelantadas debe fallar"""
        # Configurar escenario
        posiciones = self.__tablero__._obtener_posiciones_ref()
        for i in range(24):
            posiciones[i] = 0
        posiciones[20] = 2
        posiciones[22] = 2  # Ficha más adelantada
        
        # Intentar bear-off desde 20 con dado 6 teniendo fichas en 22
        es_valido, mensaje = self.__validador__.validar_movimiento(20, 6)
        self.assertFalse(es_valido)
        self.assertIn("adelantada", mensaje.lower())
    
    def test_indice_entrada_blancas(self):
        """Test: Cálculo de índice de entrada para blancas"""
        # Blancas entran por 0-5 (dados 1-6)
        self.assertEqual(self.__validador__.indice_entrada(1, 1), 0)
        self.assertEqual(self.__validador__.indice_entrada(1, 6), 5)
    
    def test_indice_entrada_negras(self):
        """Test: Cálculo de índice de entrada para negras"""
        # Negras entran por 23-18 (dados 1-6)
        self.__gestor_turnos__.cambiar_turno()  # Cambiar a negras
        self.assertEqual(self.__validador__.indice_entrada(-1, 1), 23)
        self.assertEqual(self.__validador__.indice_entrada(-1, 6), 18)
    
    def test_indice_entrada_dado_invalido(self):
        """Test: Índice de entrada con dado inválido debe lanzar ValueError"""
        with self.assertRaises(ValueError):
            self.__validador__.indice_entrada(1, 0)
        
        with self.assertRaises(ValueError):
            self.__validador__.indice_entrada(1, 7)
    
    def test_validar_entrada_barra_destino_libre(self):
        """Test: Entrada desde barra a destino libre debe ser válida"""
        # Colocar ficha en barra
        barra = self.__tablero__._obtener_barra_ref()
        barra['blancas'] = 1
        
        # Entrar con dado 3 (índice 2 para blancas)
        es_valido, mensaje = self.__validador__.validar_entrada_barra(3)
        self.assertTrue(es_valido)
    
    def test_validar_entrada_barra_destino_bloqueado(self):
        """Test: Entrada desde barra a destino bloqueado debe fallar"""
        # Colocar ficha en barra
        barra = self.__tablero__._obtener_barra_ref()
        barra['blancas'] = 1
        
        # Bloquear entrada con 2 fichas negras en posición 5 (dado 6)
        posiciones = self.__tablero__._obtener_posiciones_ref()
        posiciones[5] = -2
        
        es_valido, mensaje = self.__validador__.validar_entrada_barra(6)
        self.assertFalse(es_valido)
        self.assertIn("bloqueada", mensaje.lower())