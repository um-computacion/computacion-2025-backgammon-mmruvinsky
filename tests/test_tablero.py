from unittest import TestCase
from core.tablero import Tablero

class TestTablero(TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test_inicializar_posiciones(self):
        posiciones_esperadas = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5,
                                -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
        self.assertEqual(self.tablero.inicializar_posiciones(), posiciones_esperadas)