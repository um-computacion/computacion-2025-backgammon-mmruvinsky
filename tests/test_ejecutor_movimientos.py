from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos  
from source.ejecutor_movimientos import EjecutorMovimientos
import unittest

class TestEjecutorMovimientos(unittest.TestCase):
    """
    Tests para EjecutorMovimientos.
    
    Cobertura:
    - Ejecución de movimiento normal
    - Ejecución de captura (comer ficha)
    - Ejecución de bear-off
    - Ejecución de entrada desde barra
    - Detección de victoria
    """
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.__tablero__ = Tablero()
        self.__gestor_turnos__ = GestorTurnos()
        self.__ejecutor__ = EjecutorMovimientos(self.__tablero__, self.__gestor_turnos__)
    
    def test_ejecutar_movimiento_normal(self):
        """Test: Movimiento normal debe actualizar posiciones correctamente"""
        # Verificar posición inicial
        posiciones_antes = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_antes[0], 2)  # 2 blancas en posición 0
        self.assertEqual(posiciones_antes[3], 0)  # Vacía
        
        # Ejecutar movimiento de 0 a 3 (dado 3)
        resultado = self.__ejecutor__.ejecutar_movimiento(0, 3)
        
        # Verificar resultado
        self.assertEqual(resultado, "movió")
        
        # Verificar posiciones después
        posiciones_despues = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_despues[0], 1)  # Queda 1 blanca
        self.assertEqual(posiciones_despues[3], 1)  # 1 blanca movida
    
    def test_ejecutar_movimiento_con_captura(self):
        """Test: Movimiento que captura ficha rival debe enviarla a barra"""
        # Configurar escenario: blanca en 0, negra sola en 3
        posiciones = self.__tablero__._obtener_posiciones_ref()
        posiciones[3] = -1  # 1 ficha negra (blot)
        
        # Verificar barra inicial
        barra_antes = self.__tablero__.obtener_barra()
        self.assertEqual(barra_antes['negras'], 0)
        
        # Ejecutar captura
        resultado = self.__ejecutor__.ejecutar_movimiento(0, 3)
        
        # Verificar resultado
        self.assertEqual(resultado, "movió y comió")
        
        # Verificar barra después
        barra_despues = self.__tablero__.obtener_barra()
        self.assertEqual(barra_despues['negras'], 1)
        
        # Verificar posiciones
        posiciones_despues = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_despues[0], 1)  # Queda 1 blanca
        self.assertEqual(posiciones_despues[3], 1)  # 1 blanca (capturó)
    
    def test_ejecutar_bear_off(self):
        """Test: Bear-off debe incrementar fichas fuera"""
        # Configurar todas las blancas en home
        posiciones = self.__tablero__._obtener_posiciones_ref()
        for i in range(24):
            posiciones[i] = 0
        posiciones[20] = 1  # 1 blanca en posición 20
        
        # Verificar fichas fuera inicial
        fichas_fuera_antes = self.__tablero__.obtener_fichas_fuera()
        self.assertEqual(fichas_fuera_antes['blancas'], 0)
        
        # Ejecutar bear-off desde 20 con dado 4
        resultado = self.__ejecutor__.ejecutar_movimiento(20, 4)
        
        # Verificar resultado
        self.assertEqual(resultado, "sacó ficha")
        
        # Verificar fichas fuera después
        fichas_fuera_despues = self.__tablero__.obtener_fichas_fuera()
        self.assertEqual(fichas_fuera_despues['blancas'], 1)
        
        # Verificar que la ficha salió del tablero
        posiciones_despues = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_despues[20], 0)
    
    def test_ejecutar_bear_off_victoria(self):
        """Test: Bear-off de última ficha debe anunciar victoria"""
        # Configurar: 14 fichas fuera, 1 en tablero
        posiciones = self.__tablero__._obtener_posiciones_ref()
        for i in range(24):
            posiciones[i] = 0
        posiciones[23] = 1  # Última blanca
        
        fichas_fuera = self.__tablero__._obtener_fichas_fuera_ref()
        fichas_fuera['blancas'] = 14
        
        # Ejecutar bear-off final
        resultado = self.__ejecutor__.ejecutar_movimiento(23, 1)
        
        # Verificar victoria
        self.assertIn("juego terminado", resultado.lower())
        self.assertIn("blancas ganaron", resultado.lower())
        
        # Verificar que todas las fichas están fuera
        fichas_fuera_final = self.__tablero__.obtener_fichas_fuera()
        self.assertEqual(fichas_fuera_final['blancas'], 15)
    
    def test_ejecutar_entrada_barra(self):
        """Test: Entrada desde barra debe decrementar barra y colocar ficha"""
        # Configurar: 1 blanca en barra
        barra = self.__tablero__._obtener_barra_ref()
        barra['blancas'] = 1
        
        posiciones_antes = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_antes[2], 0)  # Destino vacío
        
        # Ejecutar entrada con dado 3 (índice 2)
        resultado = self.__ejecutor__.ejecutar_entrada_barra(3)
        
        # Verificar resultado
        self.assertEqual(resultado, "entró")
        
        # Verificar barra después
        barra_despues = self.__tablero__.obtener_barra()
        self.assertEqual(barra_despues['blancas'], 0)
        
        # Verificar posición
        posiciones_despues = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_despues[2], 1)
    
    def test_ejecutar_entrada_barra_con_captura(self):
        """Test: Entrada desde barra capturando blot rival"""
        # Configurar: 1 blanca en barra, 1 negra en destino
        barra = self.__tablero__._obtener_barra_ref()
        barra['blancas'] = 1
        
        posiciones = self.__tablero__._obtener_posiciones_ref()
        posiciones[2] = -1  # Blot negra en índice 2 (dado 3)
        
        # Ejecutar entrada capturando
        resultado = self.__ejecutor__.ejecutar_entrada_barra(3)
        
        # Verificar resultado
        self.assertEqual(resultado, "entró")
        
        # Verificar barras
        barra_final = self.__tablero__.obtener_barra()
        self.assertEqual(barra_final['blancas'], 0)  # Entró
        self.assertEqual(barra_final['negras'], 1)   # Capturada
        
        # Verificar posición
        posiciones_final = self.__tablero__.obtener_posiciones()
        self.assertEqual(posiciones_final[2], 1)  # Blanca capturó
