from unittest import TestCase
from core.backgammon import Backgammon

class TestBackgammon(TestCase):
    def setUp(self):
        self.juego = Backgammon()
        # Tablero simple: 24 posiciones con 0 fichas
        self.posiciones = [0] * 24
        self.fichas_barra_blancas = 0
        self.fichas_barra_negras = 0

    def test_turno_inicial(self):
        # Convención: blancas = 1, negras = -1
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_cambiar_turno(self):
        # 1 (blancas) -> -1 (negras) -> 1 (blancas)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), -1)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_mover_a_casilla_vacia_blancas(self):
        # Blancas mueven desde la posición 1 a una casilla vacía
        self.posiciones[0] = 1  # una ficha blanca en el origen
        self.juego._Backgammon__turno__ = 1  # blancas

        exito, msg, posiciones, fb, fn = self.juego.mover(
            origen=1,
            valor_dado=3,
            posiciones=self.posiciones,
            fichas_barra_blancas=self.fichas_barra_blancas,
            fichas_barra_negras=self.fichas_barra_negras
        )

        self.assertTrue(exito)
        self.assertEqual(msg, "movió")
        self.assertEqual(posiciones[0], 0)  # salió del origen
        self.assertEqual(posiciones[3], 1)  # llegó al destino
        self.assertEqual(fb, 0)
        self.assertEqual(fn, 0)

    def test_mover_a_casilla_con_ficha_propia_blancas(self):
        # Blancas apilan sobre otra blanca
        self.posiciones[0] = 1
        self.posiciones[3] = 2  # ya hay 2 blancas en destino
        self.juego._Backgammon__turno__ = 1  # blancas

        exito, msg, posiciones, fb, fn = self.juego.mover(1, 3, self.posiciones, 0, 0)

        self.assertTrue(exito)
        self.assertEqual(msg, "movió")
        self.assertEqual(posiciones[3], 3)  # ahora hay 3 blancas

    def test_mover_y_comer_blancas(self):
        # Blancas comen una ficha negra
        self.posiciones[0] = 1      # origen
        self.posiciones[3] = -1     # 1 negra en destino
        self.juego._Backgammon__turno__ = 1  # blancas

        exito, msg, posiciones, fb, fn = self.juego.mover(1, 3, self.posiciones, 0, 0)

        self.assertTrue(exito)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(posiciones[3], 1)  # queda 1 blanca
        self.assertEqual(fn, 1)             # negra a la barra

    def test_mover_a_posicion_bloqueada_blancas(self):
        # Blancas intentan moverse donde hay 3 negras (bloqueado)
        self.posiciones[0] = 1
        self.posiciones[3] = -3
        self.juego._Backgammon__turno__ = 1  # blancas

        exito, msg, posiciones, fb, fn = self.juego.mover(1, 3, self.posiciones, 0, 0)

        self.assertFalse(exito)
        self.assertEqual(msg, "bloqueado")
        self.assertEqual(posiciones[0], 1)   # no se mueve
        self.assertEqual(posiciones[3], -3)  # sigue igual

    def test_movimiento_fuera_del_tablero_blancas(self):
        # Blancas en la posición 23 intentan avanzar 6 posiciones → inválido
        self.posiciones[22] = 1
        self.juego._Backgammon__turno__ = 1  # blancas

        exito, msg, posiciones, fb, fn = self.juego.mover(23, 6, self.posiciones, 0, 0)

        self.assertFalse(exito)
        self.assertEqual(msg, "movimiento fuera del tablero")
        self.assertEqual(posiciones[22], 1)

    def test_mover_a_casilla_vacia_negras(self):
        # Negras (jugador = -1) mueven desde la posición 24 hacia la izquierda
        self.posiciones[23] = -1  # una ficha negra en el origen (punto 24)
        self.juego._Backgammon__turno__ = -1  # negras

        exito, msg, posiciones, fb, fn = self.juego.mover(
            origen=24,
            valor_dado=3,  # 24 -> 21 (índice 23 -> 20)
            posiciones=self.posiciones,
            fichas_barra_blancas=self.fichas_barra_blancas,
            fichas_barra_negras=self.fichas_barra_negras
        )

        self.assertTrue(exito)
        self.assertEqual(msg, "movió")
        self.assertEqual(posiciones[23], 0)   # sale del origen
        self.assertEqual(posiciones[20], -1)  # llega al destino
        self.assertEqual(fb, 0)
        self.assertEqual(fn, 0)

if __name__ == '__main__':
    import unittest
    unittest.main()