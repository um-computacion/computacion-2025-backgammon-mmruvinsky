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
    
    def test_obtener_fichas_fuera___inicial(self):
        """Test: Las fichas fuera deben ser 0 al inicio del juego"""
        fichas_fuera = self.tablero.obtener_fichas_fuera()
        
        # Verificar que retorna un diccionario
        self.assertIsInstance(fichas_fuera, dict)
        
        # Verificar que tiene las claves correctas
        self.assertIn('blancas', fichas_fuera)
        self.assertIn('negras', fichas_fuera)
        
        # Verificar que inicia en 0
        self.assertEqual(fichas_fuera['blancas'], 0)
        self.assertEqual(fichas_fuera['negras'], 0)
    
    def test_obtener_fichas_fuera___retorna_copia(self):
        """Test: El método debe retornar una copia, no la referencia original"""
        fichas_fuera1 = self.tablero.obtener_fichas_fuera()
        fichas_fuera2 = self.tablero.obtener_fichas_fuera()
        
        # Deben ser objetos diferentes (diferentes referencias)
        self.assertIsNot(fichas_fuera1, fichas_fuera2)
        
        # Pero con el mismo contenido
        self.assertEqual(fichas_fuera1, fichas_fuera2)
    
    def test_modificar_copia_no_afecta_original(self):
        """Test: Modificar la copia retornada no debe afectar el estado interno"""
        # Obtener copia
        fichas_fuera = self.tablero.obtener_fichas_fuera()
        
        # Modificar la copia
        fichas_fuera['blancas'] = 5
        fichas_fuera['negras'] = 3
        
        # Verificar que el estado interno no cambió
        fichas_fuera_nueva = self.tablero.obtener_fichas_fuera()
        self.assertEqual(fichas_fuera_nueva['blancas'], 0)
        self.assertEqual(fichas_fuera_nueva['negras'], 0)
    
    def test_obtener_fichas_fuera___con_modificaciones(self):
        """Test: El método debe reflejar cambios en el estado interno"""
        # Modificar directamente el estado interno (simulando bear-off)
        self.tablero.__fichas_fuera__['blancas'] = 7
        self.tablero.__fichas_fuera__['negras'] = 3
        
        # Obtener fichas fuera
        fichas_fuera = self.tablero.obtener_fichas_fuera()
        
        # Verificar que refleja los cambios
        self.assertEqual(fichas_fuera['blancas'], 7)
        self.assertEqual(fichas_fuera['negras'], 3)
    
    def test_obtener_fichas_fuera___valores_maximos(self):
        """Test: Verificar comportamiento con valores máximos (15 fichas)"""
        # Simular todas las fichas fuera del juego
        self.tablero.__fichas_fuera__['blancas'] = 15
        self.tablero.__fichas_fuera__['negras'] = 15
        
        fichas_fuera = self.tablero.obtener_fichas_fuera()
        
        self.assertEqual(fichas_fuera['blancas'], 15)
        self.assertEqual(fichas_fuera['negras'], 15)