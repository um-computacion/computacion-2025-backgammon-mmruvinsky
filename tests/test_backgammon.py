# tests/test_backgammon.py
import unittest
from unittest.mock import patch
from source.backgammon import Backgammon
from source.excepciones import (
    OrigenInvalidoError,
    DestinoBloquedoError,   # ojo: nombre con 'e' tal como está en tu código
    DadoNoDisponibleError,
    BearOffInvalidoError,
    MovimientoInvalidoError,
)


class TestBackgammon(unittest.TestCase):
    def setUp(self):
        self.juego = Backgammon()
        self.pos = self.juego.__tablero__.__posiciones__

        # Dejo todo el tablero en 0 para controlar cada caso
        for i in range(24):
            self.pos[i] = 0

        # Reset barras / fuera / movimientos / turno
        self.juego.__tablero__.__barra__['blancas'] = 0
        self.juego.__tablero__.__barra__['negras'] = 0
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 0
        self.juego.__tablero__.__fichas_fuera__['negras'] = 0
        self.juego.__movimientos_pendientes__ = []
        self.juego.__turno__ = 1  # blancas

    # ---------- Turnos y dados ----------
    def test_turno_y_finalizar_tirada(self):
        self.assertEqual(self.juego.obtener_turno(), 1)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), -1)
        self.juego.__movimientos_pendientes__ = [3]
        self.juego.finalizar_tirada()
        self.assertEqual(self.juego.obtener_turno(), 1)  # volvió a blancas
        self.assertEqual(self.juego.__movimientos_pendientes__, [])

    def test_tirar_dados_no_dobles(self):
        with patch('source.backgammon.Dados.tirar', return_value=(2, 5)):
            d1, d2 = self.juego.tirar_dados()
        self.assertEqual((d1, d2), (2, 5))
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [2, 5])

    def test_tirar_dados_dobles(self):
        with patch('source.backgammon.Dados.tirar', return_value=(4, 4)):
            d1, d2 = self.juego.tirar_dados()
        self.assertEqual((d1, d2), (4, 4))
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [4, 4, 4, 4])

    def test_obtener_y_consumir_movimientos(self):
        self.juego.__movimientos_pendientes__ = [5, 5, 3]
        copia = self.juego.obtener_movimientos_pendientes()
        copia.append(9)
        # No debe afectar el interno:
        self.assertEqual(self.juego.__movimientos_pendientes__, [5, 5, 3])

        # Consumir uno solo (dobles):
        self.assertTrue(self.juego.consumir_movimiento(5))
        self.assertEqual(self.juego.__movimientos_pendientes__, [5, 3])

        # Consumir inexistente:
        self.assertFalse(self.juego.consumir_movimiento(6))
        self.assertEqual(self.juego.__movimientos_pendientes__, [5, 3])

        # Disponibilidad:
        self.assertTrue(self.juego.movimientos_disponibles())
        self.juego.__movimientos_pendientes__.clear()
        self.assertFalse(self.juego.movimientos_disponibles())

    # ---------- Helper índice de entrada ----------
    def test_indice_entrada_ok_y_error(self):
        # Blancas: dado -> idx = dado - 1
        self.assertEqual(self.juego.__indice_entrada__(1, 1), 0)
        self.assertEqual(self.juego.__indice_entrada__(1, 6), 5)
        # Negras: dado -> idx = 24 - dado
        self.assertEqual(self.juego.__indice_entrada__(-1, 1), 23)
        self.assertEqual(self.juego.__indice_entrada__(-1, 6), 18)
        # Error de rango de dado
        with self.assertRaises(ValueError) as cm:
            self.juego.__indice_entrada__(1, 0)
        self.assertEqual(str(cm.exception), "dado inválido (1..6)")

    # ---------- Mover: validación de dado y barra prioritaria ----------
    def test_mover_dado_no_disponible(self):
        # Hay ficha y el dado 5 NO está disponible
        self.pos[0] = 1
        self.juego.__movimientos_pendientes__ = [3, 4]
        with self.assertRaises(DadoNoDisponibleError) as cm:
            self.juego.mover(origen=1, valor_dado=5)
        self.assertEqual(str(cm.exception), "dado no disponible para este movimiento")
        self.assertEqual(self.pos[0], 1)

    def test_mover_prioriza_entrada_desde_barra_blancas(self):
        self.juego.__tablero__.__barra__['blancas'] = 1
        self.juego.__movimientos_pendientes__ = [3, 6]
        self.assertEqual(self.pos[2], 0)  # idx entrada blancas con 3
        msg = self.juego.mover(origen=1, valor_dado=3)  # debe entrar, no mover esa ficha
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)
        self.assertNotIn(3, self.juego.__movimientos_pendientes__)
        self.assertIn(6, self.juego.__movimientos_pendientes__)

    def test_mover_prioriza_entrada_desde_barra_negras(self):
        self.juego.__turno__ = -1
        self.juego.__tablero__.__barra__['negras'] = 1
        self.juego.__movimientos_pendientes__ = [3]
        self.assertEqual(self.pos[21], 0)  # idx entrada negras con 3
        msg = self.juego.mover(origen=24, valor_dado=3)  # debe entrar
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[21], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 0)
        self.assertEqual(self.juego.__movimientos_pendientes__, [])

    # ---------- Mover: origen inválido ----------
    def test_mover_origen_invalido_vacio_y_oponente(self):
        self.juego.__movimientos_pendientes__ = [3]
        # Vacío
        self.pos[0] = 0
        with self.assertRaises(OrigenInvalidoError) as cm1:
            self.juego.mover(origen=1, valor_dado=3)
        self.assertEqual(str(cm1.exception), "origen inválido o sin fichas propias")
        # Oponente
        self.pos[0] = -1
        with self.assertRaises(OrigenInvalidoError) as cm2:
            self.juego.mover(origen=1, valor_dado=3)
        self.assertEqual(str(cm2.exception), "origen inválido o sin fichas propias")

    # ---------- Mover: bloqueado / comer / normal (blancas y negras) ----------
    def test_mover_bloqueado_blancas(self):
        self.juego.__movimientos_pendientes__ = [3]
        self.pos[0] = 1
        self.pos[3] = -3
        with self.assertRaises(DestinoBloquedoError) as cm:
            self.juego.mover(origen=1, valor_dado=3)
        self.assertEqual(str(cm.exception), "posición de destino bloqueada")
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.pos[3], -3)

    def test_mover_blancas_comer(self):
        self.juego.__movimientos_pendientes__ = [3]
        self.pos[0] = 1
        self.pos[3] = -1
        msg = self.juego.mover(origen=1, valor_dado=3)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 1)
        self.assertEqual(self.juego.__movimientos_pendientes__, [])

    def test_mover_blancas_normal_vacia_y_propia(self):
        self.juego.__movimientos_pendientes__ = [3]
        # a vacía
        self.pos[0] = 1
        msg = self.juego.mover(origen=1, valor_dado=3)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        # a propia
        self.juego.__movimientos_pendientes__ = [3]
        self.pos[0] = 1
        self.pos[3] = 2
        msg2 = self.juego.mover(origen=1, valor_dado=3)
        self.assertEqual(msg2, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 3)

    def test_mover_bloqueado_negras_comer_y_normal(self):
        # bloqueado
        self.juego.__turno__ = -1
        self.juego.__movimientos_pendientes__ = [3]
        self.pos[23] = -1
        self.pos[20] = 3
        with self.assertRaises(DestinoBloquedoError):
            self.juego.mover(origen=24, valor_dado=3)
        # comer
        self.juego.__movimientos_pendientes__ = [3]
        self.pos[23] = -1
        self.pos[20] = 1
        msg = self.juego.mover(origen=24, valor_dado=3)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[23], 0)
        self.assertEqual(self.pos[20], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 1)
        # normal
        self.juego.__movimientos_pendientes__ = [3]
        self.pos[23] = -1
        self.pos[20] = 0
        msg2 = self.juego.mover(origen=24, valor_dado=3)
        self.assertEqual(msg2, "movió")
        self.assertEqual(self.pos[23], 0)
        self.assertEqual(self.pos[20], -1)

    # ---------- Bear-off: inválido / válido / ganar (blancas y negras) ----------
    def test_bear_off_blancas_invalido(self):
        self.juego.__movimientos_pendientes__ = [5]
        self.juego.__turno__ = 1
        # una blanca en home (punto 21 = idx 20) y otra blanca fuera de home (idx 10)
        self.pos[20] = 1
        self.pos[10] = 1
        with self.assertRaises(BearOffInvalidoError) as cm:
            self.juego.mover(origen=21, valor_dado=5)  # 20 + 5 -> fuera
        self.assertEqual(str(cm.exception), "no todas las fichas están en home")
        self.assertEqual(self.pos[20], 1)

    def test_bear_off_blancas_valido_y_consumo(self):
        self.juego.__movimientos_pendientes__ = [5]
        self.juego.__turno__ = 1
        # todas en home (no hay blancas fuera de idx 18..23), sólo 1 ficha en idx 20
        self.pos[20] = 1
        msg = self.juego.mover(origen=21, valor_dado=5)
        self.assertEqual(msg, "sacó ficha")
        self.assertEqual(self.pos[20], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 1)
        self.assertNotIn(5, self.juego.__movimientos_pendientes__)

    def test_bear_off_blancas_ganar(self):
        self.juego.__movimientos_pendientes__ = [5]
        self.juego.__turno__ = 1
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 14
        self.pos[20] = 1
        msg = self.juego.mover(origen=21, valor_dado=5)
        self.assertEqual(msg, "juego terminado! Blancas ganaron")
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 15)

    def test_bear_off_negras_invalido(self):
        self.juego.__movimientos_pendientes__ = [4]
        self.juego.__turno__ = -1
        # una negra en home (punto 4 = idx 3) y otra negra fuera de home (idx 20)
        self.pos[3] = -1
        self.pos[20] = -1
        with self.assertRaises(BearOffInvalidoError) as cm:
            self.juego.mover(origen=4, valor_dado=4)  # 3 - 4 -> fuera
        self.assertEqual(str(cm.exception), "no todas las fichas están en home")
        self.assertEqual(self.pos[3], -1)

    def test_bear_off_negras_valido_y_consumo(self):
        self.juego.__movimientos_pendientes__ = [4]
        self.juego.__turno__ = -1
        self.pos[3] = -1
        msg = self.juego.mover(origen=4, valor_dado=4)
        self.assertEqual(msg, "sacó ficha")
        self.assertEqual(self.pos[3], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 1)
        self.assertNotIn(4, self.juego.__movimientos_pendientes__)

    def test_bear_off_negras_ganar(self):
        self.juego.__movimientos_pendientes__ = [4]
        self.juego.__turno__ = -1
        self.juego.__tablero__.__fichas_fuera__['negras'] = 14
        self.pos[3] = -1
        msg = self.juego.mover(origen=4, valor_dado=4)
        self.assertEqual(msg, "juego terminado! Negras ganaron")
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 15)

    # ---------- Entrar desde barra: libre / bloqueado / comer / fuera (forzado) ----------
    def test_entrar_desde_barra_blancas_libre_bloqueado_y_comer(self):
        # libre
        self.juego.__turno__ = 1
        self.juego.__tablero__.__barra__['blancas'] = 1
        msg = self.juego.entrar_desde_barra(3)  # idx 2
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)

        # bloqueado (>=2 del rival)
        self.juego.__tablero__.__barra__['blancas'] = 1
        self.pos[2] = -2
        with self.assertRaises(DestinoBloquedoError) as cm:
            self.juego.entrar_desde_barra(3)
        self.assertEqual(str(cm.exception), "posición de destino bloqueada")
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 1)

        # comer (blot)
        self.pos[2] = -1
        msg2 = self.juego.entrar_desde_barra(3)
        self.assertEqual(msg2, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)

    def test_entrar_desde_barra_negras_libre_bloqueado_y_comer(self):
        self.juego.__turno__ = -1
        # libre
        self.juego.__tablero__.__barra__['negras'] = 1
        msg = self.juego.entrar_desde_barra(3)  # idx 21
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[21], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 0)

        # bloqueado
        self.juego.__tablero__.__barra__['negras'] = 1
        self.pos[21] = 2
        with self.assertRaises(DestinoBloquedoError):
            self.juego.entrar_desde_barra(3)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 1)

        # comer
        self.pos[21] = 1
        msg2 = self.juego.entrar_desde_barra(3)
        self.assertEqual(msg2, "entró")
        self.assertEqual(self.pos[21], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 0)

    def test_entrar_desde_barra_destino_fuera_del_tablero_forzado(self):
        # Forzamos un índice imposible parcheando el helper (no está name-mangled)
        self.juego.__turno__ = 1
        self.juego.__tablero__.__barra__['blancas'] = 1
        original = self.juego.__indice_entrada__
        try:
            self.juego.__indice_entrada__ = lambda jugador, dado: 99
            with self.assertRaises(MovimientoInvalidoError) as cm:
                self.juego.entrar_desde_barra(3)
            self.assertEqual(str(cm.exception), "movimiento fuera del tablero")
            self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 1)
        finally:
            self.juego.__indice_entrada__ = original


if __name__ == "__main__":
    unittest.main()
