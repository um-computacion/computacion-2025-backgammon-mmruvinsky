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

    def test_hay_fichas_en_barra_color_invalido(self):
        """Test hay_fichas_en_barra lanza ValueError con color inválido"""
        with self.assertRaises(ValueError) as cm:
            self.tablero.hay_fichas_en_barra('rojas')
        self.assertIn("Color inválido", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            self.tablero.hay_fichas_en_barra('azules')
        self.assertIn("Color inválido", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            self.tablero.hay_fichas_en_barra('')
        self.assertIn("Color inválido", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            self.tablero.hay_fichas_en_barra('BLANCAS')  # case sensitive
        self.assertIn("Color inválido", str(cm.exception))

    def test_obtener_ficha_en_posicion_valida(self):
        """Test obtener_ficha_en_posicion con posiciones válidas"""
        # Verificar posiciones iniciales según configuración estándar
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(0), 2)   # 2 blancas
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(5), -5)  # 5 negras
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(11), 5)  # 5 blancas
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(23), -2) # 2 negras
        
        # Posiciones vacías
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(1), 0)
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(10), 0)
        
        # Modificar una posición y verificar
        self.tablero.__posiciones__[15] = 3
        self.assertEqual(self.tablero.obtener_ficha_en_posicion(15), 3)

    def test_obtener_ficha_en_posicion_fuera_de_rango(self):
        """Test obtener_ficha_en_posicion lanza IndexError fuera de rango"""
        # Índice negativo
        with self.assertRaises(IndexError) as cm:
            self.tablero.obtener_ficha_en_posicion(-1)
        self.assertIn("fuera de rango", str(cm.exception))
        
        # Índice >= CASILLEROS (24)
        with self.assertRaises(IndexError) as cm:
            self.tablero.obtener_ficha_en_posicion(24)
        self.assertIn("fuera de rango", str(cm.exception))
        
        with self.assertRaises(IndexError) as cm:
            self.tablero.obtener_ficha_en_posicion(100)
        self.assertIn("fuera de rango", str(cm.exception))
        
        # Verificar mensaje específico
        with self.assertRaises(IndexError) as cm:
            self.tablero.obtener_ficha_en_posicion(25)
        self.assertIn("Posición 25 fuera de rango [0, 23]", str(cm.exception))

    def test_metodos_protegidos_retornan_referencias(self):
        """Test que métodos _ref retornan referencias directas, no copias"""
        # _obtener_posiciones_ref
        pos_ref1 = self.tablero._obtener_posiciones_ref()
        pos_ref2 = self.tablero._obtener_posiciones_ref()
        self.assertIs(pos_ref1, pos_ref2)  # Misma referencia
        
        # Modificar ref debe afectar el interno
        pos_ref1[0] = 999
        self.assertEqual(self.tablero.__posiciones__[0], 999)
        
        # _obtener_barra_ref
        barra_ref1 = self.tablero._obtener_barra_ref()
        barra_ref2 = self.tablero._obtener_barra_ref()
        self.assertIs(barra_ref1, barra_ref2)
        
        # Modificar ref debe afectar el interno
        barra_ref1['blancas'] = 77
        self.assertEqual(self.tablero.__barra__['blancas'], 77)
        
        # _obtener_fichas_fuera_ref
        fuera_ref1 = self.tablero._obtener_fichas_fuera_ref()
        fuera_ref2 = self.tablero._obtener_fichas_fuera_ref()
        self.assertIs(fuera_ref1, fuera_ref2)
        
        # Modificar ref debe afectar el interno
        fuera_ref1['negras'] = 88
        self.assertEqual(self.tablero.__fichas_fuera__['negras'], 88)

    def test_inicializar_posiciones_configuracion_estandar(self):
        """Test verificación exhaustiva de configuración inicial estándar"""
        posiciones = self.tablero.inicializar_posiciones()
        
        # Verificar total de fichas (15 por lado)
        total_blancas = sum(p for p in posiciones if p > 0)
        total_negras = sum(abs(p) for p in posiciones if p < 0)
        
        self.assertEqual(total_blancas, 15)
        self.assertEqual(total_negras, 15)
        
        # Verificar posiciones específicas blancas
        self.assertEqual(posiciones[0], 2)
        self.assertEqual(posiciones[11], 5)
        self.assertEqual(posiciones[16], 3)
        self.assertEqual(posiciones[18], 5)
        
        # Verificar posiciones específicas negras
        self.assertEqual(posiciones[5], -5)
        self.assertEqual(posiciones[7], -3)
        self.assertEqual(posiciones[12], -5)
        self.assertEqual(posiciones[23], -2)
        
        # Verificar longitud
        self.assertEqual(len(posiciones), CASILLEROS)

    def test_inicializacion_completa_tablero(self):
        """Test que __init__ inicializa correctamente todos los atributos"""
        nuevo_tablero = Tablero()
        
        # Verificar posiciones
        self.assertIsNotNone(nuevo_tablero.__posiciones__)
        self.assertEqual(len(nuevo_tablero.__posiciones__), CASILLEROS)
        
        # Verificar barra
        self.assertIsNotNone(nuevo_tablero.__barra__)
        self.assertEqual(nuevo_tablero.__barra__['blancas'], 0)
        self.assertEqual(nuevo_tablero.__barra__['negras'], 0)
        
        # Verificar fichas fuera
        self.assertIsNotNone(nuevo_tablero.__fichas_fuera__)
        self.assertEqual(nuevo_tablero.__fichas_fuera__['blancas'], 0)
        self.assertEqual(nuevo_tablero.__fichas_fuera__['negras'], 0)

    def test_obtener_barra_valores_extremos(self):
        """Test obtener_barra con valores extremos"""
        # Muchas fichas en barra
        self.tablero.__barra__['blancas'] = 15
        self.tablero.__barra__['negras'] = 15
        
        barra = self.tablero.obtener_barra()
        self.assertEqual(barra['blancas'], 15)
        self.assertEqual(barra['negras'], 15)
        
        # Valores asimétricos
        self.tablero.__barra__['blancas'] = 7
        self.tablero.__barra__['negras'] = 2
        
        barra = self.tablero.obtener_barra()
        self.assertEqual(barra['blancas'], 7)
        self.assertEqual(barra['negras'], 2)