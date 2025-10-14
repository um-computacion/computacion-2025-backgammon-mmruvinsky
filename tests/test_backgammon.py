import unittest
from unittest.mock import Mock, patch, MagicMock
from source.backgammon import Backgammon
from source.excepciones import (
    DadoNoDisponibleError,
    OrigenInvalidoError,
    DestinoBloquedoError,
    BearOffInvalidoError,
    MovimientoInvalidoError
)


class TestBackgammonInicializacion(unittest.TestCase):
    """Tests para la inicialización del juego"""

    def test_inicializacion_crea_componentes(self):
        """Verifica que se inicialicen todos los componentes necesarios"""
        juego = Backgammon()
        
        # Verificar que los componentes privados existen
        self.assertTrue(hasattr(juego, '_Backgammon__tablero__'))
        self.assertTrue(hasattr(juego, '_Backgammon__dados__'))
        self.assertTrue(hasattr(juego, '_Backgammon__gestor_turnos__'))
        self.assertTrue(hasattr(juego, '_Backgammon__validador__'))
        self.assertTrue(hasattr(juego, '_Backgammon__ejecutor__'))
        self.assertTrue(hasattr(juego, '_Backgammon__analizador__'))

    def test_inicializacion_movimientos_pendientes_vacia(self):
        """Verifica que la lista de movimientos pendientes empiece vacía"""
        juego = Backgammon()
        self.assertEqual(juego.obtener_movimientos_pendientes(), [])
        self.assertFalse(juego.movimientos_disponibles())


class TestBackgammonConsultasEstado(unittest.TestCase):
    """Tests para los métodos de consulta de estado"""

    def setUp(self):
        """Configuración común para todos los tests"""
        self.juego = Backgammon()

    def test_obtener_turno(self):
        """Verifica que se pueda obtener el turno actual"""
        turno = self.juego.obtener_turno()
        self.assertIn(turno, ['blancas', 'negras'])

    def test_obtener_posiciones_retorna_lista(self):
        """Verifica que obtener_posiciones retorne una lista de 24 elementos"""
        posiciones = self.juego.obtener_posiciones()
        self.assertIsInstance(posiciones, list)
        self.assertEqual(len(posiciones), 24)

    def test_obtener_posiciones_retorna_copia(self):
        """Verifica que obtener_posiciones retorne una copia independiente"""
        posiciones1 = self.juego.obtener_posiciones()
        posiciones2 = self.juego.obtener_posiciones()
        
        self.assertEqual(posiciones1, posiciones2)
        self.assertIsNot(posiciones1, posiciones2)

    def test_obtener_barra_retorna_diccionario(self):
        """Verifica que obtener_barra retorne un diccionario con las claves correctas"""
        barra = self.juego.obtener_barra()
        
        self.assertIsInstance(barra, dict)
        self.assertIn('blancas', barra)
        self.assertIn('negras', barra)
        self.assertIsInstance(barra['blancas'], int)
        self.assertIsInstance(barra['negras'], int)

    def test_obtener_fichas_fuera_retorna_diccionario(self):
        """Verifica que obtener_fichas_fuera retorne un diccionario válido"""
        fichas_fuera = self.juego.obtener_fichas_fuera()
        
        self.assertIsInstance(fichas_fuera, dict)
        self.assertIn('blancas', fichas_fuera)
        self.assertIn('negras', fichas_fuera)

    def test_obtener_ficha_en_posicion_valida(self):
        """Verifica que se pueda obtener fichas en posición válida"""
        for posicion in range(1, 25):
            ficha = self.juego.obtener_ficha_en_posicion(posicion)
            self.assertIsInstance(ficha, int)

    def test_obtener_ficha_en_posicion_invalida_menor(self):
        """Verifica que lance error con posición < 1"""
        with self.assertRaises(ValueError) as context:
            self.juego.obtener_ficha_en_posicion(0)
        self.assertIn("entre 1 y 24", str(context.exception))

    def test_obtener_ficha_en_posicion_invalida_mayor(self):
        """Verifica que lance error con posición > 24"""
        with self.assertRaises(ValueError) as context:
            self.juego.obtener_ficha_en_posicion(25)
        self.assertIn("entre 1 y 24", str(context.exception))

    def test_tiene_fichas_en_barra_sin_parametro(self):
        """Verifica que tiene_fichas_en_barra funcione sin parámetros"""
        resultado = self.juego.tiene_fichas_en_barra()
        self.assertIsInstance(resultado, bool)

    def test_tiene_fichas_en_barra_con_color(self):
        """Verifica que tiene_fichas_en_barra funcione con color específico"""
        resultado_blancas = self.juego.tiene_fichas_en_barra('blancas')
        resultado_negras = self.juego.tiene_fichas_en_barra('negras')
        
        self.assertIsInstance(resultado_blancas, bool)
        self.assertIsInstance(resultado_negras, bool)

    def test_obtener_movimientos_pendientes_es_copia(self):
        """Verifica que obtener_movimientos_pendientes retorne una copia"""
        self.juego.tirar_dados()
        mov1 = self.juego.obtener_movimientos_pendientes()
        mov2 = self.juego.obtener_movimientos_pendientes()
        
        self.assertEqual(mov1, mov2)
        self.assertIsNot(mov1, mov2)

    def test_movimientos_disponibles_inicialmente_false(self):
        """Verifica que al inicio no hay movimientos disponibles"""
        self.assertFalse(self.juego.movimientos_disponibles())

    @patch.object(Backgammon, '_Backgammon__analizador__')
    def test_hay_movimiento_posible_delega_analizador(self, mock_analizador):
        """Verifica que hay_movimiento_posible delegue al analizador"""
        mock_analizador.hay_movimiento_posible.return_value = True
        self.juego._Backgammon__movimientos_pendientes__ = [3, 5]
        
        resultado = self.juego.hay_movimiento_posible()
        
        self.assertTrue(resultado)
        mock_analizador.hay_movimiento_posible.assert_called_once_with([3, 5])


class TestBackgammonTiradaDados(unittest.TestCase):
    """Tests para la tirada de dados"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()

    def test_tirar_dados_retorna_tupla(self):
        """Verifica que tirar_dados retorne una tupla de 2 elementos"""
        d1, d2 = self.juego.tirar_dados()
        
        self.assertIsInstance(d1, int)
        self.assertIsInstance(d2, int)
        self.assertGreaterEqual(d1, 1)
        self.assertLessEqual(d1, 6)
        self.assertGreaterEqual(d2, 1)
        self.assertLessEqual(d2, 6)

    def test_tirar_dados_sin_dobles_crea_dos_movimientos(self):
        """Verifica que tirada sin dobles cree 2 movimientos pendientes"""
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
            movimientos = self.juego.obtener_movimientos_pendientes()
            
            self.assertEqual(len(movimientos), 2)
            self.assertIn(3, movimientos)
            self.assertIn(5, movimientos)

    def test_tirar_dados_con_dobles_crea_cuatro_movimientos(self):
        """Verifica que tirada doble cree 4 movimientos iguales"""
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(4, 4)):
            self.juego.tirar_dados()
            movimientos = self.juego.obtener_movimientos_pendientes()
            
            self.assertEqual(len(movimientos), 4)
            self.assertEqual(movimientos, [4, 4, 4, 4])

    def test_tirar_dados_actualiza_movimientos_disponibles(self):
        """Verifica que después de tirar haya movimientos disponibles"""
        self.assertFalse(self.juego.movimientos_disponibles())
        self.juego.tirar_dados()
        self.assertTrue(self.juego.movimientos_disponibles())


class TestBackgammonCambioTurno(unittest.TestCase):
    """Tests para el cambio de turno"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()

    def test_cambiar_turno_alterna_jugador(self):
        """Verifica que cambiar_turno alterne entre blancas y negras"""
        turno_inicial = self.juego.obtener_turno()
        self.juego.cambiar_turno()
        turno_nuevo = self.juego.obtener_turno()
        
        self.assertNotEqual(turno_inicial, turno_nuevo)

    def test_finalizar_tirada_limpia_movimientos(self):
        """Verifica que finalizar_tirada limpie movimientos pendientes"""
        self.juego.tirar_dados()
        self.assertTrue(self.juego.movimientos_disponibles())
        
        self.juego.finalizar_tirada()
        
        self.assertFalse(self.juego.movimientos_disponibles())
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [])

    def test_finalizar_tirada_cambia_turno(self):
        """Verifica que finalizar_tirada cambie el turno"""
        turno_inicial = self.juego.obtener_turno()
        self.juego.finalizar_tirada()
        turno_nuevo = self.juego.obtener_turno()
        
        self.assertNotEqual(turno_inicial, turno_nuevo)


class TestBackgammonConsumirMovimiento(unittest.TestCase):
    """Tests para consumir movimientos"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()

    def test_consumir_movimiento_disponible(self):
        """Verifica que se pueda consumir un movimiento disponible"""
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
            
            resultado = self.juego.consumir_movimiento(3)
            
            self.assertTrue(resultado)
            self.assertNotIn(3, self.juego.obtener_movimientos_pendientes())
            self.assertIn(5, self.juego.obtener_movimientos_pendientes())

    def test_consumir_movimiento_no_disponible(self):
        """Verifica que consumir movimiento no disponible retorne False"""
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
            
            resultado = self.juego.consumir_movimiento(6)
            
            self.assertFalse(resultado)
            self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 2)

    def test_consumir_movimiento_duplicado_en_dobles(self):
        """Verifica que en dobles se consuma solo uno de los valores"""
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(4, 4)):
            self.juego.tirar_dados()
            
            self.juego.consumir_movimiento(4)
            
            self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 3)


class TestBackgammonMoverValidaciones(unittest.TestCase):
    """Tests para validaciones en el método mover"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()

    def test_mover_con_dado_no_disponible(self):
        """Verifica que lance error si el dado no está disponible"""
        with self.assertRaises(DadoNoDisponibleError):
            self.juego.mover(6, 6)

    @patch.object(Backgammon, '_validar_dado_mayor')
    @patch.object(Backgammon, 'tiene_fichas_en_barra', return_value=False)
    def test_mover_valida_dado_mayor(self, mock_barra, mock_validar):
        """Verifica que se llame a validar dado mayor"""
        with patch.object(self.juego._Backgammon__validador__, 'validar_movimiento', return_value=(True, None)):
            with patch.object(self.juego._Backgammon__ejecutor__, 'ejecutar_movimiento', return_value="movió"):
                self.juego.mover(6, 3)
                mock_validar.assert_called_once_with(3)

    @patch.object(Backgammon, '_validar_dado_mayor')
    @patch.object(Backgammon, 'tiene_fichas_en_barra', return_value=True)
    @patch.object(Backgammon, '_mover_desde_barra', return_value="entró")
    def test_mover_con_fichas_en_barra_prioriza_entrada(self, mock_mover_barra, mock_barra, mock_validar):
        """Verifica que si hay fichas en barra, se priorice la entrada"""
        resultado = self.juego.mover(1, 3)
        
        self.assertEqual(resultado, "entró")
        mock_mover_barra.assert_called_once_with(3)


class TestBackgammonMoverEjecucion(unittest.TestCase):
    """Tests para la ejecución de movimientos"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()

    @patch.object(Backgammon, '_validar_dado_mayor')
    @patch.object(Backgammon, 'tiene_fichas_en_barra', return_value=False)
    def test_mover_exitoso_consume_dado(self, mock_barra, mock_validar):
        """Verifica que un movimiento exitoso consuma el dado"""
        with patch.object(self.juego._Backgammon__validador__, 'validar_movimiento', return_value=(True, None)):
            with patch.object(self.juego._Backgammon__ejecutor__, 'ejecutar_movimiento', return_value="movió"):
                movimientos_iniciales = len(self.juego.obtener_movimientos_pendientes())
                
                self.juego.mover(6, 3)
                
                movimientos_finales = len(self.juego.obtener_movimientos_pendientes())
                self.assertEqual(movimientos_iniciales - 1, movimientos_finales)

    @patch.object(Backgammon, '_validar_dado_mayor')
    @patch.object(Backgammon, 'tiene_fichas_en_barra', return_value=False)
    def test_mover_invalido_no_consume_dado(self, mock_barra, mock_validar):
        """Verifica que un movimiento inválido no consuma el dado"""
        with patch.object(self.juego._Backgammon__validador__, 'validar_movimiento', 
                         return_value=(False, "origen sin fichas")):
            movimientos_iniciales = len(self.juego.obtener_movimientos_pendientes())
            
            with self.assertRaises(OrigenInvalidoError):
                self.juego.mover(1, 3)
            
            movimientos_finales = len(self.juego.obtener_movimientos_pendientes())
            self.assertEqual(movimientos_iniciales, movimientos_finales)


class TestBackgammonExcepciones(unittest.TestCase):
    """Tests para el mapeo de excepciones"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()

    def test_lanzar_excepcion_origen_invalido(self):
        """Verifica que se lance OrigenInvalidoError correctamente"""
        with self.assertRaises(OrigenInvalidoError):
            self.juego._lanzar_excepcion_apropiada("origen sin fichas")

    def test_lanzar_excepcion_destino_bloqueado(self):
        """Verifica que se lance DestinoBloquedoError correctamente"""
        with self.assertRaises(DestinoBloquedoError):
            self.juego._lanzar_excepcion_apropiada("posición bloqueada")

    def test_lanzar_excepcion_bearoff_invalido(self):
        """Verifica que se lance BearOffInvalidoError correctamente"""
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("no todas en home")

    def test_lanzar_excepcion_movimiento_fuera_tablero(self):
        """Verifica que se lance MovimientoInvalidoError para movimientos fuera"""
        with self.assertRaises(MovimientoInvalidoError):
            self.juego._lanzar_excepcion_apropiada("movimiento fuera del tablero")

    def test_lanzar_excepcion_generica(self):
        """Verifica que se lance MovimientoInvalidoError para errores genéricos"""
        with self.assertRaises(MovimientoInvalidoError):
            self.juego._lanzar_excepcion_apropiada("error desconocido")


class TestBackgammonMoverDesdeBarra(unittest.TestCase):
    """Tests para movimientos desde la barra"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()
        with patch.object(self.juego._Backgammon__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()

    def test_mover_desde_barra_exitoso(self):
        """Verifica entrada exitosa desde la barra"""
        with patch.object(self.juego._Backgammon__validador__, 'validar_entrada_barra', 
                         return_value=(True, None)):
            with patch.object(self.juego._Backgammon__ejecutor__, 'ejecutar_entrada_barra', 
                            return_value="entró"):
                resultado = self.juego._mover_desde_barra(3)
                
                self.assertEqual(resultado, "entró")

    def test_mover_desde_barra_destino_bloqueado(self):
        """Verifica que lance error si destino está bloqueado"""
        with patch.object(self.juego._Backgammon__validador__, 'validar_entrada_barra', 
                         return_value=(False, "posición bloqueada")):
            with self.assertRaises(DestinoBloquedoError):
                self.juego._mover_desde_barra(3)

    def test_mover_desde_barra_consume_dado(self):
        """Verifica que entrada desde barra consuma el dado"""
        with patch.object(self.juego._Backgammon__validador__, 'validar_entrada_barra', 
                         return_value=(True, None)):
            with patch.object(self.juego._Backgammon__ejecutor__, 'ejecutar_entrada_barra', 
                            return_value="entró"):
                movimientos_iniciales = len(self.juego.obtener_movimientos_pendientes())
                
                self.juego._mover_desde_barra(3)
                
                movimientos_finales = len(self.juego.obtener_movimientos_pendientes())
                self.assertEqual(movimientos_iniciales - 1, movimientos_finales)


class TestBackgammonValidarDadoMayor(unittest.TestCase):
    """Tests para la validación de dado mayor"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()

    def test_validar_dado_mayor_cuando_no_aplica(self):
        """Verifica que no lance error cuando la regla no aplica"""
        with patch.object(self.juego._Backgammon__analizador__, 'debe_usar_dado_mayor', 
                         return_value=False):
            self.juego._Backgammon__movimientos_pendientes__ = [3, 5]
            
            # No debería lanzar excepción
            self.juego._validar_dado_mayor(3)

    def test_validar_dado_mayor_cuando_usa_correcto(self):
        """Verifica que no lance error cuando usa el dado mayor"""
        with patch.object(self.juego._Backgammon__analizador__, 'debe_usar_dado_mayor', 
                         return_value=True):
            self.juego._Backgammon__movimientos_pendientes__ = [3, 5]
            
            # No debería lanzar excepción
            self.juego._validar_dado_mayor(5)

    def test_validar_dado_mayor_cuando_usa_incorrecto(self):
        """Verifica que lance error cuando no usa el dado mayor"""
        with patch.object(self.juego._Backgammon__analizador__, 'debe_usar_dado_mayor', 
                         return_value=True):
            self.juego._Backgammon__movimientos_pendientes__ = [3, 5]
            
            with self.assertRaises(DadoNoDisponibleError) as context:
                self.juego._validar_dado_mayor(3)
            
            self.assertIn("mayor", str(context.exception))


class TestBackgammonIntegracion(unittest.TestCase):
    """Tests de integración para flujos completos"""

    def setUp(self):
        """Configuración común"""
        self.juego = Backgammon()

    def test_flujo_completo_tirada_y_movimiento(self):
        """Verifica un flujo completo de tirada y movimiento"""
        # Tirar dados
        d1, d2 = self.juego.tirar_dados()
        self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 2)
        
        # Simular movimiento válido
        with patch.object(self.juego._Backgammon__validador__, 'validar_movimiento', 
                         return_value=(True, None)):
            with patch.object(self.juego._Backgammon__ejecutor__, 'ejecutar_movimiento', 
                            return_value="movió"):
                with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
                    with patch.object(self.juego, '_validar_dado_mayor'):
                        self.juego.mover(6, d1)
        
        # Verificar que se consumió un movimiento
        self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 1)

    def test_flujo_completo_finalizar_tirada(self):
        """Verifica flujo completo hasta finalizar tirada"""
        turno_inicial = self.juego.obtener_turno()
        
        # Tirar dados
        self.juego.tirar_dados()
        self.assertTrue(self.juego.movimientos_disponibles())
        
        # Finalizar tirada
        self.juego.finalizar_tirada()
        
        # Verificar estado final
        self.assertFalse(self.juego.movimientos_disponibles())
        self.assertNotEqual(turno_inicial, self.juego.obtener_turno())


if __name__ == '__main__':
    unittest.main(verbosity=2)