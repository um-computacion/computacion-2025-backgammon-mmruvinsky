from unittest import TestCase
from source.tablero import Tablero
from source.constantes import CASILLEROS

class TestTablero(TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test_inicializar_posiciones(self):
        posiciones_esperadas = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5,
                                -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
        self.assertEqual(self.tablero.inicializar_posiciones(), posiciones_esperadas)

    def test_obtener_posiciones_devuelve_copia_y_valores(self):
        # valores esperados según inicialización del propio tablero
        esperadas = self.tablero.inicializar_posiciones()

        p1 = self.tablero.obtener_posiciones()
        self.assertIsInstance(p1, list)
        self.assertEqual(len(p1), CASILLEROS)
        self.assertEqual(p1, esperadas)

        # debe ser una COPIA (no la lista interna)
        p1[0] = 999
        p2 = self.tablero.obtener_posiciones()
        self.assertEqual(p2, esperadas)        # el interno NO cambió
        self.assertNotEqual(p1, p2)            # la copia modificada difiere
        self.assertIsNot(p1, p2)               # objetos distintos

    def test_obtener_barra_devuelve_copia_y_valores(self):
        b1 = self.tablero.obtener_barra()
        self.assertIsInstance(b1, dict)
        # por defecto arranca vacía
        self.assertEqual(b1, {"blancas": 0, "negras": 0})

        # debe ser una COPIA (no el dict interno)
        b1["blancas"] = 7
        b2 = self.tablero.obtener_barra()
        self.assertEqual(b2, {"blancas": 0, "negras": 0})  # el interno NO cambió
        self.assertNotEqual(b1, b2)
        self.assertIsNot(b1, b2)