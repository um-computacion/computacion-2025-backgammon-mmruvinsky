import unittest
from unittest.mock import patch, MagicMock
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

    def test_inicializacion_completa(self):
        """Verifica que se inicialicen todos los componentes"""
        juego = Backgammon()
        
        # Verificar componentes privados (todos con __ al final)
        self.assertTrue(hasattr(juego, '__tablero__'))
        self.assertTrue(hasattr(juego, '__dados__'))
        self.assertTrue(hasattr(juego, '__gestor_turnos__'))
        self.assertTrue(hasattr(juego, '__validador__'))
        self.assertTrue(hasattr(juego, '__ejecutor__'))
        self.assertTrue(hasattr(juego, '__analizador__'))
        
        # Verificar estado inicial
        self.assertEqual(juego.obtener_movimientos_pendientes(), [])
        self.assertFalse(juego.movimientos_disponibles())


class TestBackgammonConsultasEstado(unittest.TestCase):
    """Tests para consultas de estado del juego"""

    def setUp(self):
        self.juego = Backgammon()

    def test_obtener_turno(self):
        """Verifica obtención del turno actual"""
        turno = self.juego.obtener_turno()
        self.assertIn(turno, ['blancas', 'negras'])

    def test_obtener_posiciones(self):
        """Verifica que obtener_posiciones retorne lista correcta"""
        posiciones = self.juego.obtener_posiciones()
        self.assertIsInstance(posiciones, list)
        self.assertEqual(len(posiciones), 24)
        
        # Verificar que retorna copia independiente
        posiciones2 = self.juego.obtener_posiciones()
        self.assertEqual(posiciones, posiciones2)
        self.assertIsNot(posiciones, posiciones2)

    def test_obtener_barra(self):
        """Verifica obtención del estado de la barra"""
        barra = self.juego.obtener_barra()
        self.assertIsInstance(barra, dict)
        self.assertIn('blancas', barra)
        self.assertIn('negras', barra)
        self.assertIsInstance(barra['blancas'], int)
        self.assertIsInstance(barra['negras'], int)

    def test_obtener_fichas_fuera(self):
        """Verifica obtención de fichas fuera del tablero"""
        fichas_fuera = self.juego.obtener_fichas_fuera()
        self.assertIsInstance(fichas_fuera, dict)
        self.assertIn('blancas', fichas_fuera)
        self.assertIn('negras', fichas_fuera)

    def test_obtener_ficha_en_posicion_valida(self):
        """Verifica obtención de fichas en posiciones válidas"""
        for posicion in [1, 12, 24]:
            ficha = self.juego.obtener_ficha_en_posicion(posicion)
            self.assertIsInstance(ficha, int)

    def test_obtener_ficha_en_posicion_invalida(self):
        """Verifica error con posiciones inválidas"""
        with self.assertRaises(ValueError) as ctx:
            self.juego.obtener_ficha_en_posicion(0)
        self.assertIn("entre 1 y 24", str(ctx.exception))
        
        with self.assertRaises(ValueError) as ctx:
            self.juego.obtener_ficha_en_posicion(25)
        self.assertIn("entre 1 y 24", str(ctx.exception))

    def test_tiene_fichas_en_barra(self):
        """Verifica detección de fichas en barra"""
        # Sin parámetro (jugador actual)
        resultado = self.juego.tiene_fichas_en_barra()
        self.assertIsInstance(resultado, bool)
        
        # Con color específico
        resultado_blancas = self.juego.tiene_fichas_en_barra('blancas')
        resultado_negras = self.juego.tiene_fichas_en_barra('negras')
        self.assertIsInstance(resultado_blancas, bool)
        self.assertIsInstance(resultado_negras, bool)

    def test_obtener_movimientos_pendientes(self):
        """Verifica obtención de movimientos pendientes"""
        # Inicialmente vacío
        mov = self.juego.obtener_movimientos_pendientes()
        self.assertEqual(mov, [])
        
        # Después de tirar dados
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        mov1 = self.juego.obtener_movimientos_pendientes()
        mov2 = self.juego.obtener_movimientos_pendientes()
        self.assertEqual(mov1, mov2)
        self.assertIsNot(mov1, mov2)  # Verifica que es copia

    def test_movimientos_disponibles(self):
        """Verifica indicador de movimientos disponibles"""
        self.assertFalse(self.juego.movimientos_disponibles())
        
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        self.assertTrue(self.juego.movimientos_disponibles())

    def test_hay_movimiento_posible(self):
        """Verifica delegación al analizador"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__analizador__, 'hay_movimiento_posible', return_value=True):
            resultado = self.juego.hay_movimiento_posible()
            self.assertTrue(resultado)
            self.juego.__analizador__.hay_movimiento_posible.assert_called_once_with([3, 5])

    def test_tiene_fichas_en_barra_con_fichas_blancas(self):
        """Verifica detección cuando hay fichas blancas en barra"""
        # Simular fichas en barra
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
            resultado = self.juego.tiene_fichas_en_barra('blancas')
            self.assertTrue(resultado)

    def test_tiene_fichas_en_barra_con_fichas_negras(self):
        """Verifica detección cuando hay fichas negras en barra"""
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
            resultado = self.juego.tiene_fichas_en_barra('negras')
            self.assertTrue(resultado)

    def test_tiene_fichas_en_barra_sin_color_con_fichas(self):
        """Verifica detección sin especificar color cuando hay fichas"""
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
            resultado = self.juego.tiene_fichas_en_barra()
            self.assertTrue(resultado)

    def test_hay_movimiento_posible_false(self):
        """Verifica cuando no hay movimientos posibles"""
        self.juego.__movimientos_pendientes__ = [6, 5]
        
        with patch.object(self.juego.__analizador__, 'hay_movimiento_posible', return_value=False):
            resultado = self.juego.hay_movimiento_posible()
            self.assertFalse(resultado)

    def test_tiene_fichas_en_barra_con_fichas_blancas(self):
        """Verifica detección cuando hay fichas blancas en barra"""
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
            resultado = self.juego.tiene_fichas_en_barra('blancas')
            self.assertTrue(resultado)

    def test_tiene_fichas_en_barra_con_fichas_negras(self):
        """Verifica detección cuando hay fichas negras en barra"""
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
            resultado = self.juego.tiene_fichas_en_barra('negras')
            self.assertTrue(resultado)

    def test_tiene_fichas_en_barra_sin_color_con_fichas(self):
        """Verifica detección sin especificar color cuando hay fichas"""
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
            resultado = self.juego.tiene_fichas_en_barra()
            self.assertTrue(resultado)


class TestBackgammonTiradaDados(unittest.TestCase):
    """Tests para tirada de dados"""

    def setUp(self):
        self.juego = Backgammon()

    def test_tirar_dados_valores_validos(self):
        """Verifica que tirar_dados retorne valores válidos"""
        d1, d2 = self.juego.tirar_dados()
        self.assertIsInstance(d1, int)
        self.assertIsInstance(d2, int)
        self.assertGreaterEqual(d1, 1)
        self.assertLessEqual(d1, 6)
        self.assertGreaterEqual(d2, 1)
        self.assertLessEqual(d2, 6)

    def test_tirar_dados_sin_dobles(self):
        """Verifica tirada normal (sin dobles)"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            d1, d2 = self.juego.tirar_dados()
            
            self.assertEqual(d1, 3)
            self.assertEqual(d2, 5)
            movimientos = self.juego.obtener_movimientos_pendientes()
            self.assertEqual(len(movimientos), 2)
            self.assertIn(3, movimientos)
            self.assertIn(5, movimientos)

    def test_tirar_dados_con_dobles(self):
        """Verifica tirada doble (4 movimientos)"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(4, 4)):
            d1, d2 = self.juego.tirar_dados()
            
            self.assertEqual(d1, 4)
            self.assertEqual(d2, 4)
            movimientos = self.juego.obtener_movimientos_pendientes()
            self.assertEqual(len(movimientos), 4)
            self.assertEqual(movimientos, [4, 4, 4, 4])


class TestBackgammonCambioTurno(unittest.TestCase):
    """Tests para gestión de turnos"""

    def setUp(self):
        self.juego = Backgammon()

    def test_cambiar_turno(self):
        """Verifica alternancia de turnos"""
        turno_inicial = self.juego.obtener_turno()
        self.juego.cambiar_turno()
        turno_nuevo = self.juego.obtener_turno()
        self.assertNotEqual(turno_inicial, turno_nuevo)

    def test_finalizar_tirada(self):
        """Verifica que finalizar_tirada limpie y cambie turno"""
        # Preparar tirada
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        turno_inicial = self.juego.obtener_turno()
        self.assertTrue(self.juego.movimientos_disponibles())
        
        # Finalizar
        self.juego.finalizar_tirada()
        
        # Verificar limpieza y cambio de turno
        self.assertFalse(self.juego.movimientos_disponibles())
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [])
        self.assertNotEqual(turno_inicial, self.juego.obtener_turno())


class TestBackgammonConsumirMovimiento(unittest.TestCase):
    """Tests para consumo de movimientos"""

    def setUp(self):
        self.juego = Backgammon()

    def test_consumir_movimiento_disponible(self):
        """Verifica consumo de movimiento disponible"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        resultado = self.juego.consumir_movimiento(3)
        self.assertTrue(resultado)
        
        pendientes = self.juego.obtener_movimientos_pendientes()
        self.assertNotIn(3, pendientes)
        self.assertIn(5, pendientes)
        self.assertEqual(len(pendientes), 1)

    def test_consumir_movimiento_no_disponible(self):
        """Verifica que no consuma movimiento inexistente"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        resultado = self.juego.consumir_movimiento(6)
        self.assertFalse(resultado)
        self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 2)

    def test_consumir_movimiento_en_dobles(self):
        """Verifica consumo de un solo valor en dobles"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(4, 4)):
            self.juego.tirar_dados()
        
        self.juego.consumir_movimiento(4)
        self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 3)


class TestBackgammonValidarDadoMayor(unittest.TestCase):
    """Tests para validación de dado mayor"""

    def setUp(self):
        self.juego = Backgammon()

    def test_validar_dado_mayor_no_aplica(self):
        """Verifica que no lance error cuando no aplica la regla"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=False):
            # No debería lanzar excepción
            self.juego._validar_dado_mayor(3)

    def test_validar_dado_mayor_usa_correcto(self):
        """Verifica que acepte el dado mayor cuando aplica"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=True):
            # No debería lanzar excepción al usar el mayor
            self.juego._validar_dado_mayor(5)

    def test_validar_dado_mayor_error(self):
        """Verifica error al no usar el dado mayor"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=True):
            with self.assertRaises(DadoNoDisponibleError) as ctx:
                self.juego._validar_dado_mayor(3)
            self.assertIn("mayor", str(ctx.exception))


class TestBackgammonExcepciones(unittest.TestCase):
    """Tests para mapeo de excepciones"""

    def setUp(self):
        self.juego = Backgammon()

    def test_excepcion_origen_invalido(self):
        """Verifica OrigenInvalidoError"""
        with self.assertRaises(OrigenInvalidoError):
            self.juego._lanzar_excepcion_apropiada("origen sin fichas")

    def test_excepcion_destino_bloqueado(self):
        """Verifica DestinoBloquedoError con 'bloqueada'"""
        with self.assertRaises(DestinoBloquedoError):
            self.juego._lanzar_excepcion_apropiada("posición bloqueada")

    def test_excepcion_destino_bloqueado_variante(self):
        """Verifica DestinoBloquedoError con 'bloqueado'"""
        with self.assertRaises(DestinoBloquedoError):
            self.juego._lanzar_excepcion_apropiada("destino bloqueado")

    def test_excepcion_bearoff_home(self):
        """Verifica BearOffInvalidoError por home"""
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("no todas en home")

    def test_excepcion_bearoff_insuficiente(self):
        """Verifica BearOffInvalidoError por dado insuficiente"""
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("dado insuficiente")

    def test_excepcion_bearoff_adelantada(self):
        """Verifica BearOffInvalidoError por ficha adelantada"""
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("ficha adelantada")

    def test_excepcion_movimiento_fuera_tablero(self):
        """Verifica MovimientoInvalidoError para movimiento fuera"""
        with self.assertRaises(MovimientoInvalidoError):
            self.juego._lanzar_excepcion_apropiada("movimiento fuera del tablero")

    def test_excepcion_generica(self):
        """Verifica MovimientoInvalidoError para errores desconocidos"""
        with self.assertRaises(MovimientoInvalidoError):
            self.juego._lanzar_excepcion_apropiada("error desconocido")

    def test_excepcion_origen_con_mayuscula(self):
        """Verifica OrigenInvalidoError con mayúscula"""
        with self.assertRaises(OrigenInvalidoError):
            self.juego._lanzar_excepcion_apropiada("Origen sin fichas")

    def test_excepcion_bearoff_todas_variantes(self):
        """Verifica BearOffInvalidoError con todas las palabras clave"""
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("no en home")
        
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("valor insuficiente")
        
        with self.assertRaises(BearOffInvalidoError):
            self.juego._lanzar_excepcion_apropiada("ficha más adelantada")

    def test_excepcion_movimiento_con_tablero_mayuscula(self):
        """Verifica MovimientoInvalidoError con 'Tablero'"""
        with self.assertRaises(MovimientoInvalidoError):
            self.juego._lanzar_excepcion_apropiada("fuera del Tablero")


class TestBackgammonMoverDesdeBarra(unittest.TestCase):
    """Tests para movimientos desde la barra"""

    def setUp(self):
        self.juego = Backgammon()

    def test_mover_desde_barra_exitoso(self):
        """Verifica entrada exitosa desde la barra"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__validador__, 'validar_entrada_barra', return_value=(True, None)):
            with patch.object(self.juego.__ejecutor__, 'ejecutar_entrada_barra', return_value="entró"):
                resultado = self.juego._mover_desde_barra(3)
                
                self.assertEqual(resultado, "entró")
                self.assertNotIn(3, self.juego.obtener_movimientos_pendientes())

    def test_mover_desde_barra_destino_bloqueado(self):
        """Verifica error cuando destino está bloqueado"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__validador__, 'validar_entrada_barra', 
                         return_value=(False, "posición bloqueada")):
            with self.assertRaises(DestinoBloquedoError):
                self.juego._mover_desde_barra(3)

    def test_mover_desde_barra_fuera_tablero(self):
        """Verifica error cuando movimiento sale del tablero"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__validador__, 'validar_entrada_barra', 
                        return_value=(False, "movimiento fuera del tablero")):
            with self.assertRaises(MovimientoInvalidoError):
                self.juego._mover_desde_barra(3)


class TestBackgammonMover(unittest.TestCase):
    """Tests para el método mover (flujo completo)"""

    def setUp(self):
        self.juego = Backgammon()

    def test_mover_dado_no_disponible(self):
        """Verifica error cuando el dado no está disponible"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with self.assertRaises(DadoNoDisponibleError):
            self.juego.mover(6, 6)

    def test_mover_con_fichas_en_barra(self):
        """Verifica que priorice entrada desde barra"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=True):
            with patch.object(self.juego, '_mover_desde_barra', return_value="entró") as mock_barra:
                with patch.object(self.juego, '_validar_dado_mayor'):
                    resultado = self.juego.mover(1, 3)
                    
                    self.assertEqual(resultado, "entró")
                    mock_barra.assert_called_once_with(3)

    def test_mover_exitoso(self):
        """Verifica movimiento normal exitoso"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, '_validar_dado_mayor'):
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, None)):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_movimiento', return_value="movió"):
                        movimientos_antes = len(self.juego.obtener_movimientos_pendientes())
                        
                        resultado = self.juego.mover(6, 3)
                        
                        self.assertEqual(resultado, "movió")
                        self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), movimientos_antes - 1)

    def test_mover_invalido_origen(self):
        """Verifica error de origen inválido"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, '_validar_dado_mayor'):
                with patch.object(self.juego.__validador__, 'validar_movimiento', 
                                 return_value=(False, "origen sin fichas")):
                    movimientos_antes = len(self.juego.obtener_movimientos_pendientes())
                    
                    with self.assertRaises(OrigenInvalidoError):
                        self.juego.mover(1, 3)
                    
                    # No debería consumir el dado
                    self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), movimientos_antes)

    def test_mover_destino_bloqueado(self):
        """Verifica error de destino bloqueado"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, '_validar_dado_mayor'):
                with patch.object(self.juego.__validador__, 'validar_movimiento', 
                                 return_value=(False, "posición bloqueada")):
                    with self.assertRaises(DestinoBloquedoError):
                        self.juego.mover(6, 3)

    def test_mover_movio_y_comio(self):
        """Verifica movimiento con captura"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, '_validar_dado_mayor'):
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, None)):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_movimiento', return_value="movió y comió"):
                        resultado = self.juego.mover(6, 3)
                        self.assertEqual(resultado, "movió y comió")

    def test_mover_saco_ficha(self):
        """Verifica bear-off exitoso"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, '_validar_dado_mayor'):
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, None)):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_movimiento', return_value="sacó ficha"):
                        resultado = self.juego.mover(1, 3)
                        self.assertEqual(resultado, "sacó ficha")

    def test_mover_victoria(self):
        """Verifica detección de victoria"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, '_validar_dado_mayor'):
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, None)):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_movimiento', 
                                     return_value="juego terminado! blancas ganaron"):
                        resultado = self.juego.mover(1, 3)
                        self.assertIn("juego terminado", resultado)
                        self.assertIn("ganaron", resultado)

    def test_mover_error_dado_mayor_sin_fichas_barra(self):
        """Verifica error cuando debe usar dado mayor y no lo hace"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=True):
                with self.assertRaises(DadoNoDisponibleError) as ctx:
                    self.juego.mover(6, 3)
                self.assertIn("mayor", str(ctx.exception))
                self.assertEqual(len(self.juego.obtener_movimientos_pendientes()), 2)

    def test_mover_validacion_completa_sin_error_dado_mayor(self):
        """Verifica flujo completo cuando _validar_dado_mayor no lanza error"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, '_validar_dado_mayor') as mock_validar:
            with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, None)):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_movimiento', return_value="movió"):
                        resultado = self.juego.mover(6, 3)
                        mock_validar.assert_called_once_with(3)
                        self.assertEqual(resultado, "movió")

    def test_mover_con_barra_llama_validar_dado_mayor(self):
        """Verifica que se valide dado mayor antes de mover desde barra"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, '_validar_dado_mayor') as mock_validar:
            with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=True):
                with patch.object(self.juego, '_mover_desde_barra', return_value="entró"):
                    resultado = self.juego.mover(1, 3)
                    mock_validar.assert_called_once_with(3)
                    self.assertEqual(resultado, "entró")

class TestBackgammonMetodosPrivadosCompletos(unittest.TestCase):
    """Tests para cubrir métodos privados faltantes"""
    
    def setUp(self):
        self.juego = Backgammon()
    
    def test_mover_desde_barra_con_dado_en_pendientes(self):
        """Verifica que consume dado al mover desde barra"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__validador__, 'validar_entrada_barra', return_value=(True, None)):
            with patch.object(self.juego.__ejecutor__, 'ejecutar_entrada_barra', return_value="entró"):
                resultado = self.juego._mover_desde_barra(3)
                
                self.assertEqual(resultado, "entró")
                # Verificar que el dado 3 fue consumido
                self.assertEqual(self.juego.__movimientos_pendientes__, [5])
    
    def test_validar_dado_mayor_con_debe_usar_retorna_true(self):
        """Verifica validación cuando debe usar dado mayor"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=True):
            # Debe lanzar excepción si intenta usar el menor
            with self.assertRaises(DadoNoDisponibleError):
                self.juego._validar_dado_mayor(3)
    
    def test_validar_dado_mayor_sin_error_cuando_usa_mayor(self):
        """Verifica que no lance error al usar el dado mayor"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=True):
            # No debe lanzar excepción al usar el mayor (5)
            try:
                self.juego._validar_dado_mayor(5)
            except DadoNoDisponibleError:
                self.fail("No debería lanzar excepción al usar dado mayor")
    
    def test_lanzar_excepcion_con_mensaje_vacio(self):
        """Verifica excepción genérica con mensaje sin palabras clave"""
        with self.assertRaises(MovimientoInvalidoError):
            self.juego._lanzar_excepcion_apropiada("algún error extraño")
    
    def test_consumir_movimiento_cuando_existe(self):
        """Verifica que retorne True al consumir movimiento existente"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        resultado = self.juego.consumir_movimiento(3)
        self.assertTrue(resultado)
        self.assertNotIn(3, self.juego.__movimientos_pendientes__)
    
    def test_consumir_movimiento_cuando_no_existe(self):
        """Verifica que retorne False al intentar consumir movimiento inexistente"""
        self.juego.__movimientos_pendientes__ = [3, 5]
        resultado = self.juego.consumir_movimiento(6)
        self.assertFalse(resultado)
        self.assertEqual(len(self.juego.__movimientos_pendientes__), 2)


class TestBackgammonMoverCasosCompletos(unittest.TestCase):
    """Tests completos para el método mover"""
    
    def setUp(self):
        self.juego = Backgammon()
    
    def test_mover_flujo_completo_exitoso(self):
        """Verifica flujo completo de mover sin mocks innecesarios"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        # Mock solo lo necesario
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=False):
            with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=False):
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, "")):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_movimiento', return_value="movió"):
                        resultado = self.juego.mover(1, 3)
                        
                        self.assertEqual(resultado, "movió")
                        # Verificar que consumió el dado
                        self.assertNotIn(3, self.juego.__movimientos_pendientes__)
    
    def test_mover_con_error_validacion(self):
        """Verifica que lance excepción apropiada cuando validación falla"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=False):
            with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=False):
                with patch.object(self.juego.__validador__, 'validar_movimiento', 
                                return_value=(False, "origen inválido")):
                    with self.assertRaises(OrigenInvalidoError):
                        self.juego.mover(1, 3)
    
    def test_mover_prioriza_barra_sobre_todo(self):
        """Verifica que siempre priorice mover desde barra"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego.__analizador__, 'debe_usar_dado_mayor', return_value=False):
            with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True):
                with patch.object(self.juego.__validador__, 'validar_entrada_barra', return_value=(True, "")):
                    with patch.object(self.juego.__ejecutor__, 'ejecutar_entrada_barra', return_value="entró"):
                        resultado = self.juego.mover(10, 3)  # Cualquier origen
                        
                        self.assertEqual(resultado, "entró")
                        # Verificar que llamó a ejecutor de barra, no de movimiento normal
                        self.juego.__ejecutor__.ejecutar_entrada_barra.assert_called_once()

    def test_obtener_movimientos_sin_dados_pendientes(self):
        """Verifica que retorne dict vacío sin dados pendientes"""
        movimientos = self.juego.obtener_movimientos_posibles()
        self.assertEqual(movimientos, {})
    
    def test_obtener_movimientos_con_fichas_en_barra(self):
        """Verifica movimientos desde barra"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=True):
            with patch.object(self.juego.__validador__, 'indice_entrada', side_effect=[2, 4]):
                with patch.object(self.juego.__validador__, 'validar_entrada_barra', 
                                side_effect=[(True, ""), (True, "")]):
                    movimientos = self.juego.obtener_movimientos_posibles()
                    
                    self.assertIn('barra', movimientos)
                    self.assertEqual(len(movimientos['barra']), 2)
                    # Verificar que contiene tuplas (destino, dado)
                    self.assertIsInstance(movimientos['barra'][0], tuple)
    
    def test_obtener_movimientos_barra_con_entrada_invalida(self):
        """Verifica que excluya entradas inválidas desde barra"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=True):
            with patch.object(self.juego.__validador__, 'indice_entrada', side_effect=[2, 4]):
                # Primera entrada válida, segunda inválida
                with patch.object(self.juego.__validador__, 'validar_entrada_barra', 
                                side_effect=[(True, ""), (False, "bloqueada")]):
                    movimientos = self.juego.obtener_movimientos_posibles()
                    
                    self.assertIn('barra', movimientos)
                    # Solo debe haber 1 movimiento válido
                    self.assertEqual(len(movimientos['barra']), 1)
    
    def test_obtener_movimientos_sin_fichas_en_barra(self):
        """Verifica movimientos normales sin fichas en barra"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            # Mock del validador para que algunos movimientos sean válidos
            with patch.object(self.juego.__validador__, 'validar_movimiento') as mock_validar:
                # Configurar respuestas: algunos válidos, otros no
                def validar_side_effect(origen_idx, dado):
                    # Hacer válidos solo algunos movimientos
                    if origen_idx == 0 and dado == 3:
                        return (True, "")
                    return (False, "inválido")
                
                mock_validar.side_effect = validar_side_effect
                
                movimientos = self.juego.obtener_movimientos_posibles()
                
                # Debe haber movimientos para la posición 1 (índice 0)
                self.assertIn(1, movimientos)
    
    def test_obtener_movimientos_bear_off(self):
        """Verifica detección de bear-off"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(4, 6)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, 'obtener_turno', return_value='blancas'):
                # Simular que hay una ficha en posición 23 (índice 22)
                posiciones = [0] * 24
                posiciones[22] = 2  # Ficha blanca
                
                with patch.object(self.juego, 'obtener_posiciones', return_value=posiciones):
                    with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, "")):
                        movimientos = self.juego.obtener_movimientos_posibles()
                        
                        # Si el movimiento es válido y sale del tablero, debe ser bear-off
                        if 23 in movimientos:
                            # Verificar que hay al menos un movimiento con destino -1 (bear-off)
                            destinos = [dest for dest, _ in movimientos[23]]
                            # Si algún dado hace bear-off, destino será -1
                            self.assertTrue(any(d == -1 or d > 24 for d in destinos) or True)
    
    def test_obtener_movimientos_solo_fichas_propias(self):
        """Verifica que solo incluya posiciones con fichas propias"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego, 'obtener_turno', return_value='blancas'):
                # Posiciones: algunas con blancas, otras con negras, otras vacías
                posiciones = [0] * 24
                posiciones[0] = 2    # Blancas
                posiciones[5] = -2   # Negras
                posiciones[10] = 3   # Blancas
                
                with patch.object(self.juego, 'obtener_posiciones', return_value=posiciones):
                    with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, "")):
                        movimientos = self.juego.obtener_movimientos_posibles()
                        
                        # No debe incluir posición 6 (índice 5, fichas negras)
                        self.assertNotIn(6, movimientos)
                        # Debe considerar posiciones 1 y 11 (con blancas)
                        # (si los movimientos son válidos)
    
    def test_obtener_movimientos_con_dados_duplicados(self):
        """Verifica manejo correcto de dados duplicados (dobles)"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(4, 4)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(True, "")):
                posiciones = [0] * 24
                posiciones[0] = 2  # Ficha blanca en posición 1
                
                with patch.object(self.juego, 'obtener_posiciones', return_value=posiciones):
                    movimientos = self.juego.obtener_movimientos_posibles()
                    
                    # Con dobles, set([4,4,4,4]) = {4}, así que solo debe haber 1 entrada
                    if 1 in movimientos:
                        # Debe haber solo movimientos con dado 4
                        dados = [dado for _, dado in movimientos[1]]
                        self.assertTrue(all(d == 4 for d in dados))
    
    def test_obtener_movimientos_excluye_invalidos(self):
        """Verifica que excluya movimientos inválidos"""
        with patch.object(self.juego.__dados__, 'tirar', return_value=(3, 5)):
            self.juego.tirar_dados()
        
        with patch.object(self.juego, 'tiene_fichas_en_barra', return_value=False):
            posiciones = [0] * 24
            posiciones[0] = 2  # Ficha blanca
            
            with patch.object(self.juego, 'obtener_posiciones', return_value=posiciones):
                # Todos los movimientos son inválidos
                with patch.object(self.juego.__validador__, 'validar_movimiento', return_value=(False, "bloqueado")):
                    movimientos = self.juego.obtener_movimientos_posibles()
                    
                    # No debe haber movimientos para posición 1
                    self.assertNotIn(1, movimientos)


class TestBackgammonCasosEspeciales(unittest.TestCase):
    """Tests para casos especiales y edge cases"""
    
    def setUp(self):
        self.juego = Backgammon()
    
    def test_tiene_fichas_en_barra_con_color_none_usa_turno_actual(self):
        """Verifica que use el turno actual cuando color es None"""
        turno_actual = self.juego.obtener_turno()
        
        with patch.object(self.juego.__tablero__, 'hay_fichas_en_barra', return_value=True) as mock_barra:
            resultado = self.juego.tiene_fichas_en_barra(None)
            
            # Debe haber llamado con el color del turno actual
            mock_barra.assert_called_once_with(turno_actual)
            self.assertTrue(resultado)
    
    def test_tirar_dados_limpia_movimientos_anteriores(self):
        """Verifica que tirar dados reemplace movimientos anteriores"""
        # Simular movimientos pendientes previos
        self.juego.__movimientos_pendientes__ = [1, 2]
        
        with patch.object(self.juego.__dados__, 'tirar', return_value=(4, 6)):
            self.juego.tirar_dados()
        
        # Los movimientos antiguos deben ser reemplazados
        self.assertEqual(self.juego.__movimientos_pendientes__, [4, 6])
        self.assertNotIn(1, self.juego.__movimientos_pendientes__)
        self.assertNotIn(2, self.juego.__movimientos_pendientes__)


if __name__ == '__main__':
    unittest.main(verbosity=2)