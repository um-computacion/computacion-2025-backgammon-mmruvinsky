from unittest import TestCase
from source.backgammon import Backgammon

class TestBackgammon(TestCase):
    def setUp(self):
        self.juego = Backgammon()
        self.pos = self.juego.__tablero__.__posiciones__
        for i in range(24):
            self.pos[i] = 0
        self.juego.__fichas_barra_blancas__ = 0
        self.juego.__fichas_barra_negras__ = 0
        # turno por defecto: blancas (1)

    def test_turno_inicial(self):
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_cambiar_turno(self):
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), -1)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_mover_a_casilla_vacia_blancas(self):
        self.pos[0] = 1
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(origen=1, valor_dado=3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        self.assertEqual(self.juego.__fichas_barra_blancas__, 0)
        self.assertEqual(self.juego.__fichas_barra_negras__, 0)

    def test_mover_a_casilla_con_ficha_propia_blancas(self):
        self.pos[0] = 1
        self.pos[3] = 2
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(1, 3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 3)

    def test_mover_y_comer_blancas(self):
        self.pos[0] = 1
        self.pos[3] = -1
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(1, 3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        self.assertEqual(self.juego.__fichas_barra_negras__, 1)

    def test_mover_a_posicion_bloqueada_blancas(self):
        self.pos[0] = 1
        self.pos[3] = -3
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(1, 3)

        self.assertFalse(ok)
        self.assertEqual(msg, "posición de destino bloqueada")
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.pos[3], -3)

    def test_movimiento_fuera_del_tablero_blancas(self):
        self.pos[22] = 1
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(23, 6)

        self.assertFalse(ok)
        self.assertEqual(msg, "movimiento fuera del tablero")
        self.assertEqual(self.pos[22], 1)

    def test_mover_a_casilla_vacia_negras(self):
        self.pos[23] = -1
        self.juego.__turno__ = -1

        ok, msg = self.juego.mover(origen=24, valor_dado=3)  # 23 -> 20

        self.assertTrue(ok)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[23], 0)
        self.assertEqual(self.pos[20], -1)
        self.assertEqual(self.juego.__fichas_barra_blancas__, 0)
        self.assertEqual(self.juego.__fichas_barra_negras__, 0)

    def test_mover_y_comer_negras(self):
        self.pos[23] = -1
        self.pos[20] = 1
        self.juego.__turno__ = -1

        ok, msg = self.juego.mover(24, 3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[23], 0)
        self.assertEqual(self.pos[20], -1)
        self.assertEqual(self.juego.__fichas_barra_blancas__, 1)

    def test_bloqueo_negras(self):
        self.pos[23] = -1
        self.pos[20] = 3
        self.juego.__turno__ = -1

        ok, msg = self.juego.mover(24, 3)

        self.assertFalse(ok)
        self.assertEqual(msg, "posición de destino bloqueada")
        self.assertEqual(self.pos[23], -1)
        self.assertEqual(self.pos[20], 3)

    def test_entrar_desde_barra_blancas_libre(self):
        self.juego.__turno__ = 1
        self.juego.__fichas_barra_blancas__ = 1

        ok, msg = self.juego.entrar_desde_barra(3)  # índice 2

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__fichas_barra_blancas__, 0)

    def test_entrar_desde_barra_blancas_bloqueado(self):
        self.juego.__turno__ = 1
        self.juego.__fichas_barra_blancas__ = 1
        self.pos[2] = -2  # bloqueado

        ok, msg = self.juego.entrar_desde_barra(3)

        self.assertFalse(ok)
        self.assertEqual(msg, "posición de destino bloqueada")
        self.assertEqual(self.juego.__fichas_barra_blancas__, 1)

    def test_entrar_desde_barra_blancas_comer(self):
        self.juego.__turno__ = 1
        self.juego.__fichas_barra_blancas__ = 1
        self.pos[2] = -1  # blot

        ok, msg = self.juego.entrar_desde_barra(3)

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__fichas_barra_blancas__, 0)
        self.assertEqual(self.juego.__fichas_barra_negras__, 1)

    def test_entrar_desde_barra_negras_libre(self):
        self.juego.__turno__ = -1
        self.juego.__fichas_barra_negras__ = 1

        ok, msg = self.juego.entrar_desde_barra(3)  # 24-3 = 21

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[21], -1)
        self.assertEqual(self.juego.__fichas_barra_negras__, 0)

    def test_mover_con_fichas_en_barra_deriva_a_entrar(self):
        self.juego.__turno__ = 1
        self.juego.__fichas_barra_blancas__ = 1
        # destino índice 2 libre por defecto
        ok, msg = self.juego.mover(origen=1, valor_dado=3)
        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__fichas_barra_blancas__, 0)

if __name__ == '__main__':
    import unittest
    unittest.main()