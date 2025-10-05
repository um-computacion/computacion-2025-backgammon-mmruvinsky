from source.gestor_turnos import GestorTurnos
import unittest

class TestGestorTurnos(unittest.TestCase):
    """
    Tests para GestorTurnos.
    
    Cobertura:
    - Inicialización correcta
    - Cambio de turno
    - Obtención de turno (string)
    - Obtención de dirección (int)
    - Validación de turno específico
    """
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.__gestor__ = GestorTurnos()
    
    def test_inicializacion_turno_blancas(self):
        """Test: El juego debe iniciar con turno de blancas"""
        self.assertEqual(self.__gestor__.obtener_turno(), "blancas")
        self.assertEqual(self.__gestor__.obtener_direccion(), 1)
    
    def test_cambiar_turno_blancas_a_negras(self):
        """Test: Cambiar de blancas a negras"""
        self.__gestor__.cambiar_turno()
        self.assertEqual(self.__gestor__.obtener_turno(), "negras")
        self.assertEqual(self.__gestor__.obtener_direccion(), -1)
    
    def test_cambiar_turno_negras_a_blancas(self):
        """Test: Cambiar de negras a blancas"""
        self.__gestor__.cambiar_turno()  # Blancas -> Negras
        self.__gestor__.cambiar_turno()  # Negras -> Blancas
        self.assertEqual(self.__gestor__.obtener_turno(), "blancas")
        self.assertEqual(self.__gestor__.obtener_direccion(), 1)
    
    def test_cambios_multiples_turno(self):
        """Test: Múltiples cambios de turno deben alternar correctamente"""
        turnos_esperados = ["blancas", "negras", "blancas", "negras", "blancas"]
        
        for turno_esperado in turnos_esperados:
            self.assertEqual(self.__gestor__.obtener_turno(), turno_esperado)
            self.__gestor__.cambiar_turno()
    
    def test_direccion_consistente_con_turno(self):
        """Test: La dirección debe ser consistente con el turno"""
        # Blancas: dirección = 1
        self.assertEqual(self.__gestor__.obtener_direccion(), 1)
        
        # Negras: dirección = -1
        self.__gestor__.cambiar_turno()
        self.assertEqual(self.__gestor__.obtener_direccion(), -1)
    
    def test_es_turno_de_blancas_verdadero(self):
        """Test: es_turno_de debe retornar True cuando es turno de blancas"""
        self.assertTrue(self.__gestor__.es_turno_de("blancas"))
        self.assertFalse(self.__gestor__.es_turno_de("negras"))
    
    def test_es_turno_de_negras_verdadero(self):
        """Test: es_turno_de debe retornar True cuando es turno de negras"""
        self.__gestor__.cambiar_turno()
        self.assertTrue(self.__gestor__.es_turno_de("negras"))
        self.assertFalse(self.__gestor__.es_turno_de("blancas"))
    
    def test_es_turno_de_color_invalido(self):
        """Test: es_turno_de debe lanzar ValueError con color inválido"""
        with self.assertRaises(ValueError):
            self.__gestor__.es_turno_de("rojas")
        
        with self.assertRaises(ValueError):
            self.__gestor__.es_turno_de("")
        
        with self.assertRaises(ValueError):
            self.__gestor__.es_turno_de("BLANCAS")  # Case sensitive