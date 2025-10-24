import unittest
from unittest.mock import patch, MagicMock
from source.analizador_posibilidades import AnalizadorPosibilidades
from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos


class TestAnalizadorPosibilidadesInicializacion(unittest.TestCase):
    """Tests para inicialización"""
    
    def test_inicializacion(self):
        """Verifica inicialización correcta"""
        tablero = Tablero()
        gestor = GestorTurnos()
        analizador = AnalizadorPosibilidades(tablero, gestor)
        
        self.assertTrue(hasattr(analizador, '__tablero__'))
        self.assertTrue(hasattr(analizador, '__gestor_turnos__'))


class TestAnalizadorPuedeUsarDado(unittest.TestCase):
    """Tests para puede_usar_dado"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_puede_usar_dado_con_fichas_en_barra(self):
        """Verifica que priorice entrada desde barra"""
        with patch.object(self.analizador, '_hay_en_barra', return_value=True):
            with patch.object(self.analizador, '_puede_entrar_desde_barra', return_value=True):
                resultado = self.analizador.puede_usar_dado(3)
                self.assertTrue(resultado)
    
    def test_puede_usar_dado_sin_fichas_en_barra_movimiento_valido(self):
        """Verifica movimiento normal válido"""
        with patch.object(self.analizador, '_hay_en_barra', return_value=False):
            with patch.object(self.gestor, 'obtener_direccion', return_value=1):
                # Configurar tablero con ficha blanca en posición 0
                pos = self.tablero._obtener_posiciones_ref()
                for i in range(24):
                    pos[i] = 0
                pos[0] = 2  # Blancas en posición 0
                
                resultado = self.analizador.puede_usar_dado(3)
                self.assertTrue(resultado)
    
    def test_puede_usar_dado_destino_bloqueado(self):
        """Verifica cuando destino está bloqueado"""
        with patch.object(self.analizador, '_hay_en_barra', return_value=False):
            with patch.object(self.gestor, 'obtener_direccion', return_value=1):
                pos = self.tablero._obtener_posiciones_ref()
                for i in range(24):
                    pos[i] = 0
                pos[0] = 2   # Blancas en 0
                pos[3] = -2  # Negras bloquean posición 3
                
                resultado = self.analizador.puede_usar_dado(3)
                self.assertFalse(resultado)
    
    def test_puede_usar_dado_bear_off_valido(self):
        """Verifica bear-off válido"""
        with patch.object(self.analizador, '_hay_en_barra', return_value=False):
            with patch.object(self.gestor, 'obtener_direccion', return_value=1):
                with patch.object(self.analizador, '_todas_en_home', return_value=True):
                    pos = self.tablero._obtener_posiciones_ref()
                    for i in range(24):
                        pos[i] = 0
                    pos[20] = 2  # Blancas en home
                    
                    with patch.object(self.analizador, '_puede_hacer_bear_off', return_value=True):
                        resultado = self.analizador.puede_usar_dado(4)
                        self.assertTrue(resultado)
    
    def test_puede_usar_dado_sin_movimientos(self):
        """Verifica cuando no hay movimientos posibles"""
        with patch.object(self.analizador, '_hay_en_barra', return_value=False):
            with patch.object(self.gestor, 'obtener_direccion', return_value=1):
                pos = self.tablero._obtener_posiciones_ref()
                for i in range(24):
                    pos[i] = 0
                # Sin fichas propias
                
                resultado = self.analizador.puede_usar_dado(3)
                self.assertFalse(resultado)


class TestAnalizadorPuedeUsarAmbos(unittest.TestCase):
    """Tests para puede_usar_ambos_dados"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_puede_usar_ambos_dados_iguales(self):
        """Verifica que siempre retorne True con dobles"""
        resultado = self.analizador.puede_usar_ambos_dados(4, 4)
        self.assertTrue(resultado)
    
    def test_puede_usar_ambos_orden_1_2(self):
        """Verifica uso en orden 1-2"""
        with patch.object(self.analizador, '_puede_usar_dado_tras_simular', 
                         side_effect=[True, False]):
            resultado = self.analizador.puede_usar_ambos_dados(3, 5)
            self.assertTrue(resultado)
    
    def test_puede_usar_ambos_orden_2_1(self):
        """Verifica uso en orden 2-1"""
        with patch.object(self.analizador, '_puede_usar_dado_tras_simular', 
                         side_effect=[False, True]):
            resultado = self.analizador.puede_usar_ambos_dados(3, 5)
            self.assertTrue(resultado)
    
    def test_no_puede_usar_ambos(self):
        """Verifica cuando no puede usar en ningún orden"""
        with patch.object(self.analizador, '_puede_usar_dado_tras_simular', 
                         return_value=False):
            resultado = self.analizador.puede_usar_ambos_dados(3, 5)
            self.assertFalse(resultado)


class TestAnalizadorDebeUsarDadoMayor(unittest.TestCase):
    """Tests para debe_usar_dado_mayor"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_debe_usar_dado_mayor_no_dos_dados(self):
        """Verifica que retorne False si no hay exactamente 2 dados"""
        self.assertFalse(self.analizador.debe_usar_dado_mayor([3]))
        self.assertFalse(self.analizador.debe_usar_dado_mayor([3, 3, 3, 3]))
    
    def test_debe_usar_dado_mayor_dobles(self):
        """Verifica que retorne False con dobles"""
        resultado = self.analizador.debe_usar_dado_mayor([4, 4])
        self.assertFalse(resultado)
    
    def test_debe_usar_dado_mayor_puede_ambos(self):
        """Verifica False cuando puede usar ambos"""
        with patch.object(self.analizador, 'puede_usar_dado', return_value=True):
            with patch.object(self.analizador, 'puede_usar_ambos_dados', return_value=True):
                resultado = self.analizador.debe_usar_dado_mayor([3, 5])
                self.assertFalse(resultado)
    
    def test_debe_usar_dado_mayor_solo_uno_posible(self):
        """Verifica True cuando solo puede uno pero no ambos"""
        with patch.object(self.analizador, 'puede_usar_dado', return_value=True):
            with patch.object(self.analizador, 'puede_usar_ambos_dados', return_value=False):
                resultado = self.analizador.debe_usar_dado_mayor([3, 5])
                self.assertTrue(resultado)
    
    def test_debe_usar_dado_mayor_ninguno_posible(self):
        """Verifica False cuando no puede usar ninguno"""
        with patch.object(self.analizador, 'puede_usar_dado', return_value=False):
            with patch.object(self.analizador, 'puede_usar_ambos_dados', return_value=False):
                resultado = self.analizador.debe_usar_dado_mayor([3, 5])
                self.assertFalse(resultado)
    
    def test_debe_usar_dado_mayor_solo_primero(self):
        """Verifica False cuando solo puede usar el primero"""
        with patch.object(self.analizador, 'puede_usar_dado', side_effect=[True, False]):
            with patch.object(self.analizador, 'puede_usar_ambos_dados', return_value=False):
                resultado = self.analizador.debe_usar_dado_mayor([3, 5])
                self.assertFalse(resultado)


class TestAnalizadorHayMovimientoPosible(unittest.TestCase):
    """Tests para hay_movimiento_posible"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_hay_movimiento_sin_pendientes(self):
        """Verifica False cuando no hay pendientes"""
        resultado = self.analizador.hay_movimiento_posible([])
        self.assertFalse(resultado)
    
    def test_hay_movimiento_posible_con_uno(self):
        """Verifica True cuando hay movimiento posible"""
        with patch.object(self.analizador, 'puede_usar_dado', return_value=True):
            resultado = self.analizador.hay_movimiento_posible([3, 5])
            self.assertTrue(resultado)
    
    def test_no_hay_movimiento_posible(self):
        """Verifica False cuando no hay movimientos"""
        with patch.object(self.analizador, 'puede_usar_dado', return_value=False):
            resultado = self.analizador.hay_movimiento_posible([3, 5])
            self.assertFalse(resultado)
    
    def test_hay_movimiento_con_duplicados(self):
        """Verifica que maneje duplicados (dobles)"""
        with patch.object(self.analizador, 'puede_usar_dado', return_value=True):
            resultado = self.analizador.hay_movimiento_posible([4, 4, 4, 4])
            self.assertTrue(resultado)


class TestAnalizadorSimulaciones(unittest.TestCase):
    """Tests para métodos de simulación"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_puede_usar_dado_tras_simular_exitoso(self):
        """Verifica simulación exitosa"""
        with patch.object(self.analizador, '_simular_mejor_movimiento', return_value=True):
            with patch.object(self.analizador, 'puede_usar_dado', return_value=True):
                resultado = self.analizador._puede_usar_dado_tras_simular(3, 5)
                self.assertTrue(resultado)
    
    def test_puede_usar_dado_tras_simular_falla_simulacion(self):
        """Verifica cuando falla la simulación"""
        with patch.object(self.analizador, '_simular_mejor_movimiento', return_value=False):
            resultado = self.analizador._puede_usar_dado_tras_simular(3, 5)
            self.assertFalse(resultado)
    
    def test_puede_usar_dado_tras_simular_restaura_estado(self):
        """Verifica que restaure el estado"""
        pos_inicial = self.tablero.obtener_posiciones().copy()
        barra_inicial = self.tablero.obtener_barra().copy()
        
        with patch.object(self.analizador, '_simular_mejor_movimiento', return_value=True):
            with patch.object(self.analizador, 'puede_usar_dado', return_value=True):
                self.analizador._puede_usar_dado_tras_simular(3, 5)
        
        # Verificar restauración
        self.assertEqual(self.tablero.obtener_posiciones(), pos_inicial)
        self.assertEqual(self.tablero.obtener_barra(), barra_inicial)
    
    def test_simular_mejor_movimiento_desde_barra(self):
        """Verifica simulación de entrada desde barra"""
        with patch.object(self.gestor, 'obtener_direccion', return_value=1):
            with patch.object(self.analizador, '_hay_en_barra', return_value=True):
                barra = self.tablero._obtener_barra_ref()
                barra['blancas'] = 1
                pos = self.tablero._obtener_posiciones_ref()
                pos[2] = 0  # Destino libre
                
                resultado = self.analizador._simular_mejor_movimiento(3)
                self.assertTrue(resultado)
    
    def test_simular_mejor_movimiento_barra_bloqueada(self):
        """Verifica simulación cuando entrada está bloqueada"""
        with patch.object(self.gestor, 'obtener_direccion', return_value=1):
            with patch.object(self.analizador, '_hay_en_barra', return_value=True):
                pos = self.tablero._obtener_posiciones_ref()
                pos[2] = -2  # Destino bloqueado
                
                resultado = self.analizador._simular_mejor_movimiento(3)
                self.assertFalse(resultado)
    
    def test_simular_mejor_movimiento_normal(self):
        """Verifica simulación de movimiento normal"""
        with patch.object(self.gestor, 'obtener_direccion', return_value=1):
            with patch.object(self.analizador, '_hay_en_barra', return_value=False):
                pos = self.tablero._obtener_posiciones_ref()
                for i in range(24):
                    pos[i] = 0
                pos[0] = 2
                pos[3] = 0
                
                resultado = self.analizador._simular_mejor_movimiento(3)
                self.assertTrue(resultado)
    
    def test_simular_mejor_movimiento_bear_off(self):
        """Verifica simulación de bear-off"""
        with patch.object(self.gestor, 'obtener_direccion', return_value=1):
            with patch.object(self.analizador, '_hay_en_barra', return_value=False):
                with patch.object(self.analizador, '_todas_en_home', return_value=True):
                    with patch.object(self.analizador, '_puede_hacer_bear_off', return_value=True):
                        pos = self.tablero._obtener_posiciones_ref()
                        for i in range(24):
                            pos[i] = 0
                        pos[20] = 2
                        
                        resultado = self.analizador._simular_mejor_movimiento(4)
                        self.assertTrue(resultado)
    
    def test_simular_mejor_movimiento_sin_opciones(self):
        """Verifica simulación sin movimientos posibles"""
        with patch.object(self.gestor, 'obtener_direccion', return_value=1):
            with patch.object(self.analizador, '_hay_en_barra', return_value=False):
                pos = self.tablero._obtener_posiciones_ref()
                for i in range(24):
                    pos[i] = 0
                
                resultado = self.analizador._simular_mejor_movimiento(3)
                self.assertFalse(resultado)


class TestAnalizadorEjecucionesSimuladas(unittest.TestCase):
    """Tests para ejecuciones simuladas"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_ejecutar_entrada_simulada_sin_captura(self):
        """Verifica entrada simulada sin captura"""
        pos = self.tablero._obtener_posiciones_ref()
        barra = self.tablero._obtener_barra_ref()
        pos[2] = 0
        barra['blancas'] = 1
        
        with patch.object(self.analizador, '_es_blot_rival', return_value=False):
            self.analizador._ejecutar_entrada_simulada(2, 1)
        
        self.assertEqual(pos[2], 1)
        self.assertEqual(barra['blancas'], 0)
    
    def test_ejecutar_entrada_simulada_con_captura(self):
        """Verifica entrada simulada con captura de blot"""
        pos = self.tablero._obtener_posiciones_ref()
        barra = self.tablero._obtener_barra_ref()
        pos[2] = -1
        barra['blancas'] = 1
        
        with patch.object(self.analizador, '_es_blot_rival', return_value=True):
            self.analizador._ejecutar_entrada_simulada(2, 1)
        
        self.assertEqual(pos[2], 1)
        self.assertEqual(barra['blancas'], 0)
        self.assertEqual(barra['negras'], 1)
    
    def test_ejecutar_entrada_simulada_negras(self):
        """Verifica entrada simulada para negras"""
        pos = self.tablero._obtener_posiciones_ref()
        barra = self.tablero._obtener_barra_ref()
        pos[21] = 0
        barra['negras'] = 1
        
        with patch.object(self.analizador, '_es_blot_rival', return_value=False):
            self.analizador._ejecutar_entrada_simulada(21, -1)
        
        self.assertEqual(pos[21], -1)
        self.assertEqual(barra['negras'], 0)
    
    def test_ejecutar_movimiento_simulado_sin_captura(self):
        """Verifica movimiento simulado sin captura"""
        pos = self.tablero._obtener_posiciones_ref()
        pos[0] = 2
        pos[3] = 0
        
        with patch.object(self.analizador, '_es_blot_rival', return_value=False):
            self.analizador._ejecutar_movimiento_simulado(0, 3, 1)
        
        self.assertEqual(pos[0], 1)
        self.assertEqual(pos[3], 1)
    
    def test_ejecutar_movimiento_simulado_con_captura(self):
        """Verifica movimiento simulado con captura"""
        pos = self.tablero._obtener_posiciones_ref()
        barra = self.tablero._obtener_barra_ref()
        pos[0] = 2
        pos[3] = -1
        
        with patch.object(self.analizador, '_es_blot_rival', return_value=True):
            self.analizador._ejecutar_movimiento_simulado(0, 3, 1)
        
        self.assertEqual(pos[0], 1)
        self.assertEqual(pos[3], 1)
        self.assertEqual(barra['negras'], 1)
    
    def test_restaurar_estado(self):
        """Verifica restauración de estado"""
        pos = self.tablero._obtener_posiciones_ref()
        barra = self.tablero._obtener_barra_ref()
        
        pos_backup = [1, 2, 3] + [0] * 21
        barra_backup = {'blancas': 2, 'negras': 3}
        
        self.analizador._restaurar_estado(pos_backup, barra_backup)
        
        self.assertEqual(pos[:3], [1, 2, 3])
        self.assertEqual(barra['blancas'], 2)
        self.assertEqual(barra['negras'], 3)


class TestAnalizadorMetodosAuxiliares(unittest.TestCase):
    """Tests para métodos auxiliares"""
    
    def setUp(self):
        self.tablero = Tablero()
        self.gestor = GestorTurnos()
        self.analizador = AnalizadorPosibilidades(self.tablero, self.gestor)
    
    def test_puede_entrar_desde_barra_valido(self):
        """Verifica entrada válida desde barra"""
        pos = self.tablero._obtener_posiciones_ref()
        pos[2] = 0
        
        resultado = self.analizador._puede_entrar_desde_barra(3, 1)
        self.assertTrue(resultado)
    
    def test_puede_entrar_desde_barra_bloqueado(self):
        """Verifica entrada bloqueada"""
        pos = self.tablero._obtener_posiciones_ref()
        pos[2] = -2
        
        resultado = self.analizador._puede_entrar_desde_barra(3, 1)
        self.assertFalse(resultado)
    
    def test_puede_entrar_desde_barra_fuera_tablero(self):
        """Verifica cuando destino está fuera del tablero"""
        with patch.object(self.analizador, '_calcular_indice_entrada', return_value=25):
            resultado = self.analizador._puede_entrar_desde_barra(6, 1)
            self.assertFalse(resultado)
    
    def test_puede_hacer_bear_off_exacto(self):
        """Verifica bear-off con distancia exacta"""
        pos = [0] * 24
        pos[20] = 2
        
        resultado = self.analizador._puede_hacer_bear_off(20, 4, 1, pos)
        self.assertTrue(resultado)
    
    def test_puede_hacer_bear_off_overshoot_valido(self):
        """Verifica bear-off con overshoot sin fichas adelantadas"""
        pos = [0] * 24
        pos[20] = 2
        
        resultado = self.analizador._puede_hacer_bear_off(20, 6, 1, pos)
        self.assertTrue(resultado)
    
    def test_puede_hacer_bear_off_overshoot_invalido(self):
        """Verifica bear-off con overshoot con fichas adelantadas"""
        pos = [0] * 24
        pos[20] = 2
        pos[22] = 1  # Ficha más adelantada
        
        resultado = self.analizador._puede_hacer_bear_off(20, 6, 1, pos)
        self.assertFalse(resultado)
    
    def test_puede_hacer_bear_off_insuficiente(self):
        """Verifica bear-off con dado insuficiente"""
        pos = [0] * 24
        pos[20] = 2
        
        resultado = self.analizador._puede_hacer_bear_off(20, 2, 1, pos)
        self.assertFalse(resultado)
    
    def test_puede_hacer_bear_off_negras_exacto(self):
        """Verifica bear-off negras con distancia exacta"""
        pos = [0] * 24
        pos[3] = -2
        
        resultado = self.analizador._puede_hacer_bear_off(3, 4, -1, pos)
        self.assertTrue(resultado)
    
    def test_puede_hacer_bear_off_negras_overshoot_valido(self):
        """Verifica bear-off negras con overshoot válido"""
        pos = [0] * 24
        pos[3] = -2
        
        resultado = self.analizador._puede_hacer_bear_off(3, 6, -1, pos)
        self.assertTrue(resultado)
    
    def test_puede_hacer_bear_off_negras_overshoot_invalido(self):
        """Verifica bear-off negras con overshoot inválido"""
        pos = [0] * 24
        pos[3] = -2
        pos[1] = -1  # Ficha más adelantada
        
        resultado = self.analizador._puede_hacer_bear_off(3, 6, -1, pos)
        self.assertFalse(resultado)
    
    def test_todas_en_home_blancas_verdadero(self):
        """Verifica todas en home para blancas"""
        pos = self.tablero._obtener_posiciones_ref()
        for i in range(18):
            pos[i] = 0
        pos[20] = 5
        
        resultado = self.analizador._todas_en_home(1)
        self.assertTrue(resultado)
    
    def test_todas_en_home_blancas_falso(self):
        """Verifica cuando no todas están en home (blancas)"""
        pos = self.tablero._obtener_posiciones_ref()
        pos[10] = 1  # Ficha fuera de home
        
        resultado = self.analizador._todas_en_home(1)
        self.assertFalse(resultado)
    
    def test_todas_en_home_negras_verdadero(self):
        """Verifica todas en home para negras"""
        pos = self.tablero._obtener_posiciones_ref()
        for i in range(6, 24):
            pos[i] = 0
        pos[3] = -5
        
        resultado = self.analizador._todas_en_home(-1)
        self.assertTrue(resultado)
    
    def test_todas_en_home_negras_falso(self):
        """Verifica cuando no todas están en home (negras)"""
        pos = self.tablero._obtener_posiciones_ref()
        pos[10] = -1  # Ficha fuera de home
        
        resultado = self.analizador._todas_en_home(-1)
        self.assertFalse(resultado)
    
    def test_hay_en_barra_blancas_true(self):
        """Verifica fichas en barra para blancas"""
        barra = self.tablero._obtener_barra_ref()
        barra['blancas'] = 1
        
        resultado = self.analizador._hay_en_barra(1)
        self.assertTrue(resultado)
    
    def test_hay_en_barra_blancas_false(self):
        """Verifica sin fichas en barra para blancas"""
        resultado = self.analizador._hay_en_barra(1)
        self.assertFalse(resultado)
    
    def test_hay_en_barra_negras_true(self):
        """Verifica fichas en barra para negras"""
        barra = self.tablero._obtener_barra_ref()
        barra['negras'] = 1
        
        resultado = self.analizador._hay_en_barra(-1)
        self.assertTrue(resultado)
    
    def test_hay_en_barra_negras_false(self):
        """Verifica sin fichas en barra para negras"""
        resultado = self.analizador._hay_en_barra(-1)
        self.assertFalse(resultado)
    
    def test_destino_bloqueado_true(self):
        """Verifica destino bloqueado"""
        resultado = self.analizador._destino_bloqueado(-2, 1)
        self.assertTrue(resultado)
    
    def test_destino_bloqueado_false_vacio(self):
        """Verifica destino no bloqueado (vacío)"""
        resultado = self.analizador._destino_bloqueado(0, 1)
        self.assertFalse(resultado)
    
    def test_destino_bloqueado_false_propio(self):
        """Verifica destino no bloqueado (fichas propias)"""
        resultado = self.analizador._destino_bloqueado(2, 1)
        self.assertFalse(resultado)
    
    def test_destino_bloqueado_false_blot(self):
        """Verifica destino no bloqueado (un solo blot)"""
        resultado = self.analizador._destino_bloqueado(-1, 1)
        self.assertFalse(resultado)
    
    def test_es_blot_rival_true(self):
        """Verifica detección de blot rival"""
        resultado = self.analizador._es_blot_rival(-1, 1)
        self.assertTrue(resultado)
    
    def test_es_blot_rival_false_vacio(self):
        """Verifica sin blot (vacío)"""
        resultado = self.analizador._es_blot_rival(0, 1)
        self.assertFalse(resultado)
    
    def test_es_blot_rival_false_propio(self):
        """Verifica sin blot (fichas propias)"""
        resultado = self.analizador._es_blot_rival(1, 1)
        self.assertFalse(resultado)
    
    def test_es_blot_rival_false_bloqueado(self):
        """Verifica sin blot (2+ fichas rivales)"""
        resultado = self.analizador._es_blot_rival(-2, 1)
        self.assertFalse(resultado)
    
    def test_calcular_indice_entrada_blancas(self):
        """Verifica cálculo de índice para blancas"""
        self.assertEqual(self.analizador._calcular_indice_entrada(1, 1), 0)
        self.assertEqual(self.analizador._calcular_indice_entrada(1, 6), 5)
    
    def test_calcular_indice_entrada_negras(self):
        """Verifica cálculo de índice para negras"""
        self.assertEqual(self.analizador._calcular_indice_entrada(-1, 1), 23)
        self.assertEqual(self.analizador._calcular_indice_entrada(-1, 6), 18)


if __name__ == '__main__':
    unittest.main(verbosity=2) 