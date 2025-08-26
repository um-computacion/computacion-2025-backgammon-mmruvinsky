from unittest import TestCase
from core.backgammon import Backgammon

class TestBackgammon(TestCase):
    def setUp(self):
        self.juego = Backgammon()

    def test_turno_inicial(self):
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_cambiar_turno(self):
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), 2)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), 1)

    