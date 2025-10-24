import unittest
from unittest.mock import patch
from source.dados import Dados

class TestDados(unittest.TestCase):
    
    def test_constructor_inicializa_dados(self):
        """Test que el constructor inicializa los dados correctamente"""
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [3, 5]  # Primer llamada devuelve 3, segunda 5
            dados = Dados()
            self.assertEqual(dados.dado1, 3)
            self.assertEqual(dados.dado2, 5)
            # Verificar que se llamó randint dos veces con los parámetros correctos
            self.assertEqual(mock_randint.call_count, 2)
            mock_randint.assert_any_call(1, 6)

    def test_propiedades_dado1_y_dado2(self):
        """Test que las propiedades devuelven los valores correctos"""
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [1, 6]
            dados = Dados()
            # Test getter properties
            self.assertEqual(dados.dado1, 1)
            self.assertEqual(dados.dado2, 6)
            
            # Verificar que son propiedades de solo lectura
            # No se pueden asignar directamente
            with self.assertRaises(AttributeError):
                dados.dado1 = 5

    def test_tirar_genera_nuevos_valores(self):
        """Test que el método tirar genera nuevos valores"""
        dados = Dados()
        
        # Mockear las llamadas a randint para tirar()
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [4, 2]
            resultado = dados.tirar()
            
            # Verificar que devuelve la tupla correcta
            self.assertEqual(resultado, (4, 2))
            
            # Verificar que los valores internos se actualizaron
            self.assertEqual(dados.dado1, 4)
            self.assertEqual(dados.dado2, 2)
            
            # Verificar que se llamó randint dos veces
            self.assertEqual(mock_randint.call_count, 2)
            mock_randint.assert_any_call(1, 6)

    def test_tirar_multiples_veces(self):
        """Test que múltiples tiradas funcionan correctamente"""
        dados = Dados()
        
        # Primera tirada
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [1, 1]
            resultado1 = dados.tirar()
            self.assertEqual(resultado1, (1, 1))
        
        # Segunda tirada con valores diferentes
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [6, 6]
            resultado2 = dados.tirar()
            self.assertEqual(resultado2, (6, 6))
            
        # Verificar que los valores se actualizaron
        self.assertEqual(dados.dado1, 6)
        self.assertEqual(dados.dado2, 6)

    def test_valores_en_rango_valido(self):
        """Test que los valores están en el rango 1-6"""
        dados = Dados()
        
        # Test inicial
        self.assertTrue(1 <= dados.dado1 <= 6)
        self.assertTrue(1 <= dados.dado2 <= 6)
        
        # Test después de tirar
        for _ in range(10):  # Tirar múltiples veces
            d1, d2 = dados.tirar()
            self.assertTrue(1 <= d1 <= 6)
            self.assertTrue(1 <= d2 <= 6)
            self.assertTrue(1 <= dados.dado1 <= 6)
            self.assertTrue(1 <= dados.dado2 <= 6)

    def test_tipos_de_datos_correctos(self):
        """Test que los dados devuelven tipos de datos correctos"""
        dados = Dados()
        
        # Verificar tipos iniciales
        self.assertIsInstance(dados.dado1, int)
        self.assertIsInstance(dados.dado2, int)
        
        # Verificar tipos después de tirar
        resultado = dados.tirar()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], int)
        self.assertIsInstance(resultado[1], int)

    def test_independencia_de_dados(self):
        """Test que los dos dados son independientes"""
        with patch('random.randint') as mock_randint:
            # Configurar valores diferentes para cada dado
            mock_randint.side_effect = [1, 6, 3, 4]  # Constructor: 1,6 - tirar(): 3,4
            
            dados = Dados()
            self.assertNotEqual(dados.dado1, dados.dado2)
            
            d1, d2 = dados.tirar()
            self.assertNotEqual(d1, d2)

if __name__ == "__main__":
    unittest.main()