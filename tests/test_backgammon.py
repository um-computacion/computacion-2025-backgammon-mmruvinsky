import unittest
from unittest.mock import patch

from source.backgammon import Backgammon
from source.constantes import CASILLEROS
from source.excepciones import (
    DadoNoDisponibleError,
    OrigenInvalidoError,
    DestinoBloquedoError,
    MovimientoInvalidoError,
    BearOffInvalidoError,
)

class TestBackgammonIntegrado(unittest.TestCase):
    def setUp(self):
        self.g = Backgammon()
        # Estado “limpio” y explícito para coherencia
        self.pos = self.g.__tablero__.__posiciones__
        self.bar = self.g.__tablero__.__barra__
        self.out = self.g.__tablero__.__fichas_fuera__
        self.pos[:] = [0] * CASILLEROS
        self.bar['blancas'] = 0
        self.bar['negras'] = 0
        self.out['blancas'] = 0
        self.out['negras'] = 0
        self.g.__movimientos_pendientes__.clear()
        self.g.__turno__ = 1  # blancas

    # ---------- Helpers básicos y validaciones ----------
    def test_indice_entrada_valido_e_invalido(self):
        self.assertEqual(self.g.__indice_entrada__(1, 1), 0)
        self.assertEqual(self.g.__indice_entrada__(1, 6), 5)
        self.assertEqual(self.g.__indice_entrada__(-1, 1), 23)
        self.assertEqual(self.g.__indice_entrada__(-1, 6), 18)
        with self.assertRaises(ValueError):
            self.g.__indice_entrada__(1, 0)
        with self.assertRaises(ValueError):
            self.g.__indice_entrada__(1, 7)

    def test_hay_en_barra(self):
        self.bar['blancas'] = 1
        self.assertTrue(self.g.__hay_en_barra__(1))
        self.bar['blancas'] = 0
        self.bar['negras'] = 2
        self.assertTrue(self.g.__hay_en_barra__(-1))
        self.bar['negras'] = 0
        self.assertFalse(self.g.__hay_en_barra__(1))
        self.assertFalse(self.g.__hay_en_barra__(-1))

    def test_todas_en_home_blancas_y_negras(self):
        # Blancas en home: no hay blancas en [0..17]
        self.assertTrue(self.g.__todas_en_home__(1))
        self.pos[10] = 1
        self.assertFalse(self.g.__todas_en_home__(1))
        self.pos[10] = 0
        # Negras en home: no hay negras en [6..23]
        self.g.__turno__ = -1
        self.assertTrue(self.g.__todas_en_home__(-1))
        self.pos[20] = -1
        self.assertFalse(self.g.__todas_en_home__(-1))

    def test_es_fuera_destino_bloqueado_blot_origen_valido(self):
        self.assertTrue(self.g._es_fuera(-1))
        self.assertTrue(self.g._es_fuera(24))
        self.assertFalse(self.g._es_fuera(0))
        self.assertTrue(self.g._destino_bloqueado(-2, 1))
        self.assertFalse(self.g._destino_bloqueado(2, 1))
        self.assertTrue(self.g._destino_es_blot_rival(-1, 1))
        self.assertFalse(self.g._destino_es_blot_rival(-2, 1))

        self.pos[0] = 1
        self.assertTrue(self.g._origen_valido(self.pos, 0, 1))
        self.assertFalse(self.g._origen_valido(self.pos, 1, 1))
        self.assertFalse(self.g._origen_valido(self.pos, -1, 1))
        self.assertFalse(self.g._origen_valido(self.pos, 24, 1))

    # ---------- Tirar/consumir dados ----------
    def test_tirar_dados_dobles_y_no_dobles(self):
        with patch.object(self.g.__dados__, 'tirar', return_value=(3, 3)):
            d1, d2 = self.g.tirar_dados()
            self.assertEqual((d1, d2), (3, 3))
            self.assertEqual(self.g.obtener_movimientos_pendientes(), [3, 3, 3, 3])
        with patch.object(self.g.__dados__, 'tirar', return_value=(2, 5)):
            d1, d2 = self.g.tirar_dados()
            self.assertEqual((d1, d2), (2, 5))
            self.assertEqual(self.g.obtener_movimientos_pendientes(), [2, 5])

    def test_consumir_movimiento_vale_y_no_vale(self):
        self.g.__movimientos_pendientes__[:] = [2, 5]
        self.assertTrue(self.g.consumir_movimiento(2))
        self.assertEqual(self.g.obtener_movimientos_pendientes(), [5])
        self.assertFalse(self.g.consumir_movimiento(6))
        self.assertEqual(self.g.obtener_movimientos_pendientes(), [5])

    # ---------- Política de uso de dados ----------
    def test_puede_usar_ambos_dados_casos(self):
        # no aplica (dobles / len != 2)
        self.g.__movimientos_pendientes__[:] = [4, 4, 4, 4]
        self.assertTrue(self.g.puede_usar_ambos_dados())
        self.g.__movimientos_pendientes__[:] = [6]
        self.assertTrue(self.g.puede_usar_ambos_dados())

        # dos distintos: se puede en algún orden
        self.g.__movimientos_pendientes__[:] = [2, 5]
        # armamos una posición factible
        self.pos[0] = 1  # blanca en 0 -> con 2 llega a 2; con 5 a 5 (ambos libres)
        self.assertTrue(self.g.puede_usar_ambos_dados())

        # dos distintos: no se puede en ningún orden (bloqueos simulados)
        with patch.object(self.g, '_puede_usar_dado', return_value=False), \
             patch.object(self.g, '_puede_usar_dado_tras_simular', return_value=False):
            self.assertFalse(self.g.puede_usar_ambos_dados())

    def test_debe_usar_dado_mayor_variantes(self):
        # len != 2
        self.g.__movimientos_pendientes__[:] = [3]
        self.assertFalse(self.g.debe_usar_dado_mayor())
        # dobles
        self.g.__movimientos_pendientes__[:] = [4, 4]
        self.assertFalse(self.g.debe_usar_dado_mayor())
        # ambos usables pero también se pueden usar ambos -> False
        self.g.__movimientos_pendientes__[:] = [2, 5]
        with patch.object(self.g, '_puede_usar_dado', return_value=True), \
             patch.object(self.g, 'puede_usar_ambos_dados', return_value=True):
            self.assertFalse(self.g.debe_usar_dado_mayor())
        # ambos usables, pero la lógica dice que no se pueden usar ambos -> True (debe elegir el mayor)
        with patch.object(self.g, '_puede_usar_dado', return_value=True), \
             patch.object(self.g, 'puede_usar_ambos_dados', return_value=False):
            self.assertTrue(self.g.debe_usar_dado_mayor())

    # ---------- Usabilidad de un dado (con y sin barra) ----------
    def test_puede_usar_dado_con_barra_destino_libre_y_bloqueado(self):
        # Hay blancas en barra
        self.bar['blancas'] = 1
        # Destino libre
        with patch.object(self.g, '__indice_entrada__', return_value=0), \
             patch.object(self.g, '_es_fuera', return_value=False), \
             patch.object(self.g, '_destino_bloqueado', return_value=False):
            self.assertTrue(self.g._puede_usar_dado(3))
        # Destino bloqueado
        with patch.object(self.g, '__indice_entrada__', return_value=0), \
             patch.object(self.g, '_es_fuera', return_value=False), \
             patch.object(self.g, '_destino_bloqueado', return_value=True):
            self.assertFalse(self.g._puede_usar_dado(3))
        # índice inválido -> except -> False
        with patch.object(self.g, '__indice_entrada__', side_effect=ValueError("mal")), \
             patch.object(self.g, '_es_fuera', return_value=True):
            self.assertFalse(self.g._puede_usar_dado(6))

    def test_puede_usar_dado_sin_barra_movimiento_y_bear_off(self):
        # Movimiento normal posible
        self.bar['blancas'] = 0
        self.pos[0] = 1
        self.assertTrue(self.g._puede_usar_dado(3))  # 0->3 libre
        # Movimiento bloqueado
        self.pos[3] = -2  # bloqueado por 2 negras
        self.assertFalse(self.g._puede_usar_dado(3))
        self.pos[3] = 0
        # Bear off posible (todas en home y needed exacto)
        self.pos[:] = [0]*CASILLEROS
        self.pos[20] = 1  # needed=4
        self.assertTrue(self.g.__todas_en_home__(1))
        self.assertTrue(self.g._puede_usar_dado(4))
        # Bear off overshoot permitido (no hay más adelantadas)
        self.assertTrue(self.g._puede_usar_dado(6))
        # Bear off overshoot no permitido si hay más adelantadas
        self.pos[22] = 1
        self.assertFalse(self.g._puede_usar_dado(6))

    def test_puede_usar_dado_tras_simular_restaura_estado(self):
        # Preparar estado y verificar restauración
        self.pos[0] = 1
        self.g.__movimientos_pendientes__[:] = [2, 5]
        pos_before = self.pos.copy()
        bar_before = self.bar.copy()
        self.g._puede_usar_dado_tras_simular(2, 5)
        self.assertEqual(self.pos, pos_before)
        self.assertEqual(self.bar, bar_before)

    # ---------- Simuladores internos ----------
    def test_ejecutar_entrada_simulada_y_movimiento_simulado(self):
        # Entrada simulada con comer blot
        self.g.__turno__ = 1
        self.bar['blancas'] = 1
        self.pos[0] = -1  # blot
        self.g._ejecutar_entrada_simulada(0)
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.bar['negras'], 1)
        self.assertEqual(self.bar['blancas'], 0)

        # Movimiento simulado: sumar propio y restar origen
        self.pos[:] = [0]*CASILLEROS
        self.pos[0] = 2
        self.pos[3] = 1
        self.g._ejecutar_movimiento_simulado(0, 3)
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.pos[3], 2)

    # ---------- finalizar_tirada ----------
    def test_finalizar_tirada_resetea_y_cambia_turno(self):
        self.g.__movimientos_pendientes__[:] = [3, 4]
        self.g.__turno__ = 1
        self.g.finalizar_tirada()
        self.assertEqual(self.g.obtener_movimientos_pendientes(), [])
        self.assertEqual(self.g.obtener_turno(), "negras")

    # ---------- Mover: política, barra, origen, bloqueos, comer, normal ----------
    def test_mover_exige_dado_mayor(self):
        self.g.__movimientos_pendientes__[:] = [3, 5]
        with patch.object(self.g, 'debe_usar_dado_mayor', return_value=True):
            with self.assertRaisesRegex(DadoNoDisponibleError, "debe usar el dado mayor"):
                self.g.mover(origen=1, valor_dado=3)

    def test_mover_prioridad_barra(self):
        self.g.__movimientos_pendientes__[:] = [3]
        self.bar['blancas'] = 1
        # entrada directa a 0 (libre)
        with patch.object(self.g, '__indice_entrada__', return_value=0):
            msg = self.g.mover(origen=6, valor_dado=3)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.bar['blancas'], 0)
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.g.obtener_movimientos_pendientes(), [])

    def test_mover_origen_invalido(self):
        self.g.__movimientos_pendientes__[:] = [3]
        with self.assertRaises(OrigenInvalidoError):
            self.g.mover(origen=1, valor_dado=3)

    def test_mover_destino_bloqueado(self):
        self.g.__movimientos_pendientes__[:] = [3]
        self.pos[0] = 1
        self.pos[3] = -2
        with self.assertRaises(DestinoBloquedoError):
            self.g.mover(origen=1, valor_dado=3)

    def test_mover_dado_no_disponible(self):
        self.g.__movimientos_pendientes__[:] = [2]
        self.pos[0] = 1
        with self.assertRaises(DadoNoDisponibleError):
            self.g.mover(origen=1, valor_dado=3)

    def test_mover_come_y_normal(self):
        # comer
        self.g.__movimientos_pendientes__[:] = [3]
        self.pos[0] = 1
        self.pos[3] = -1
        msg = self.g.mover(origen=1, valor_dado=3)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        self.assertEqual(self.g.obtener_movimientos_pendientes(), [])
        self.assertEqual(self.bar['negras'], 1)

        # normal (sumar a propia)
        self.g.__movimientos_pendientes__[:] = [2]
        self.pos[0] = 1
        self.pos[2] = 1
        msg = self.g.mover(origen=1, valor_dado=2)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[2], 2)
        self.assertEqual(self.g.obtener_movimientos_pendientes(), [])

    def test_mover_bear_off_por_fuera(self):
        # blancas todas en home y una en 20 (needed=4)
        self.g.__movimientos_pendientes__[:] = [4]
        self.pos[:] = [0]*CASILLEROS
        self.pos[20] = 1
        msg = self.g.mover(origen=21, valor_dado=4)  # origen es 1-based
        self.assertIn(msg, ("sacó ficha", "juego terminado! Blancas ganaron"))
        self.assertEqual(self.pos[20], 0)
        self.assertEqual(self.out['blancas'], 1)

    # ---------- entrar_desde_barra ----------
    def test_entrar_desde_barra_fuera_bloqueado_blot_y_libre(self):
        # fuera
        with patch.object(self.g, '__indice_entrada__', return_value=99), \
             patch.object(self.g, '_es_fuera', return_value=True):
            with self.assertRaises(MovimientoInvalidoError):
                self.g.entrar_desde_barra(3)

        # bloqueado
        with patch.object(self.g, '__indice_entrada__', return_value=0), \
             patch.object(self.g, '_es_fuera', return_value=False):
            self.pos[0] = -2
            with self.assertRaises(DestinoBloquedoError):
                self.g.entrar_desde_barra(3)

        # blot y libre
        self.g.__turno__ = -1  # ahora entran negras
        self.bar['negras'] = 2
        with patch.object(self.g, '__indice_entrada__', return_value=23), \
             patch.object(self.g, '_es_fuera', return_value=False):
            # blot: hay 1 blanca
            self.pos[23] = 1
            msg = self.g.entrar_desde_barra(1)
            self.assertEqual(msg, "entró")
            self.assertEqual(self.pos[23], -1)
            self.assertEqual(self.bar['blancas'], 1)  # blanca comida
            self.assertEqual(self.bar['negras'], 1)   # salió una negra

            # libre/propio
            self.pos[23] = -1
            msg = self.g.entrar_desde_barra(1)
            self.assertEqual(msg, "entró")
            self.assertEqual(self.pos[23], -2)
            self.assertEqual(self.bar['negras'], 0)

    # ---------- __intentar_bear_off__ ----------
    def test_bear_off_invalido_y_valido_con_final(self):
        # no todas en home
        with patch.object(self.g, '__todas_en_home__', return_value=False):
            with self.assertRaisesRegex(BearOffInvalidoError, "no todas las fichas"):
                self.g.__intentar_bear_off__(origen_idx=20, valor_dado=4)

        # valor insuficiente
        with patch.object(self.g, '__todas_en_home__', return_value=True):
            with self.assertRaisesRegex(BearOffInvalidoError, "valor insuficiente"):
                self.g.__intentar_bear_off__(origen_idx=20, valor_dado=3)

        # overshoot con “más adelantada”
        self.g.__turno__ = 1
        self.pos[:] = [0]*CASILLEROS
        self.pos[20] = 1
        self.pos[22] = 1
        with patch.object(self.g, '__todas_en_home__', return_value=True):
            with self.assertRaisesRegex(BearOffInvalidoError, "más adelantada"):
                self.g.__intentar_bear_off__(origen_idx=20, valor_dado=6)

        # camino feliz + final de juego
        self.pos[:] = [0]*CASILLEROS
        self.pos[2] = -1
        self.g.__turno__ = -1
        self.out['negras'] = 14
        with patch.object(self.g, '__todas_en_home__', return_value=True):
            msg = self.g.__intentar_bear_off__(origen_idx=2, valor_dado=3)
            self.assertEqual(self.pos[2], 0)
            self.assertEqual(self.out['negras'], 15)
            self.assertIn("ganaron", msg)

    # ---------- hay_movimiento_posible ----------
    def test_hay_movimiento_posible_variantes(self):
        self.g.__movimientos_pendientes__.clear()
        self.assertFalse(self.g.hay_movimiento_posible())

        self.g.__movimientos_pendientes__[:] = [2, 5, 5]
        # colocamos una blanca que pueda mover con 2
        self.pos[0] = 1
        self.assertTrue(self.g.hay_movimiento_posible())

        # bloqueamos todo
        with patch.object(self.g, '_puede_usar_dado', return_value=False):
            self.assertFalse(self.g.hay_movimiento_posible())


if __name__ == "__main__":
    unittest.main()



