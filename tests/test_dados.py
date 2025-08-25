from unittest import TestCase
from core.dados import Dados

class TestDados(TestCase):
    def test_dados_en_rango(self):
        dados = Dados()
        self.assertTrue(1 <= dados.dado1 <= 6, "Dado 1 fuera de rango")
        self.assertTrue(1 <= dados.dado2 <= 6, "Dado 2 fuera de rango")