import unittest
from unittest.mock import patch
from source.dados import Dados

class TestDados(unittest.TestCase):

    @patch("source.dados.random.randint")
    def test_init_y_properties(self, mock_randint):
        mock_randint.side_effect = [4, 2]     # valores al construir
        d = Dados()
        # ACCESO a las properties -> cubre líneas @property
        self.assertEqual(d.dado1, 4)
        self.assertEqual(d.dado2, 2)

    @patch("source.dados.random.randint")
    def test_tirar_actualiza_y_devuelve(self, mock_randint):
        # 1) construcción
        mock_randint.side_effect = [1, 1]
        d = Dados()

        # 2) tirar: dos llamadas nuevas
        mock_randint.side_effect = [6, 3]
        tupla = d.tirar()

        self.assertEqual(tupla, (6, 3))
        # properties reflejan el NUEVO estado -> cubre @property
        self.assertEqual(d.dado1, 6)
        self.assertEqual(d.dado2, 3)

    @patch("source.dados.random.randint")
    def test_tirar_determinista(self, mock_randint):
        mock_randint.side_effect = [2, 5]  # init
        d = Dados()
        mock_randint.side_effect = [3, 5]  # tirar
        res = d.tirar()
        self.assertEqual(res, (3, 5))
        self.assertEqual(mock_randint.call_count, 4)  # 2 en __init__ + 2 en tirar
        mock_randint.assert_any_call(1, 6)

if __name__ == "__main__":
    unittest.main()
