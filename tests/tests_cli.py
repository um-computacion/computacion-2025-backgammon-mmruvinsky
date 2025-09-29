import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
from cli.cli import BackgammonCLI

script_dir = os.path.dirname(os.path.abspath(__file__))
cli_dir = os.path.join(script_dir, "cli")
source_dir = os.path.join(script_dir, "source")
sys.path.insert(0, cli_dir)
sys.path.insert(0, source_dir)


class TestBackgammonCLI(unittest.TestCase):
    """Test suite para BackgammonCLI - Primera mitad"""
    
    def setUp(self):
        """Configuración para cada test"""
        self.cli = BackgammonCLI()
        
    def test_inicializacion_cli(self):
        """Test: Inicialización correcta del CLI"""
        # Verificar que el CLI se inicializa correctamente
        self.assertIsNotNone(self.cli.juego)
        self.assertEqual(self.cli.juego.obtener_turno(), "blancas")
        self.assertIsInstance(self.cli.comandos, dict)
        
        # Verificar que todos los comandos esperados están presentes
        comandos_esperados = ['help', 'h', 'dados', 'd', 'mover', 'm', 
                            'tablero', 't', 'estado', 'e', 'salir', 'q', 
                            'finalizar', 'f']
        for comando in comandos_esperados:
            self.assertIn(comando, self.cli.comandos)
    
    def test_obtener_posiciones_tablero(self):
        """Test: Obtener posiciones del tablero"""
        posiciones = self.cli.obtener_posiciones_tablero()
        self.assertIsInstance(posiciones, list)
        self.assertEqual(len(posiciones), 24)
        
        # Verificar posiciones iniciales conocidas
        self.assertEqual(posiciones[0], 2)    # Blancas en posición 1
        self.assertEqual(posiciones[23], -2)  # Negras en posición 24
    
    def test_obtener_barra(self):
        """Test: Obtener estado de la barra"""
        barra = self.cli.obtener_barra()
        self.assertIsInstance(barra, dict)
        self.assertIn('blancas', barra)
        self.assertIn('negras', barra)
        self.assertEqual(barra['blancas'], 0)
        self.assertEqual(barra['negras'], 0)
    
    def test_obtener_fichas_fuera(self):
        """Test: Obtener fichas fuera del tablero"""
        fichas_fuera = self.cli.obtener_fichas_fuera()
        self.assertIsInstance(fichas_fuera, dict)
        self.assertIn('blancas', fichas_fuera)
        self.assertIn('negras', fichas_fuera)
        self.assertEqual(fichas_fuera['blancas'], 0)
        self.assertEqual(fichas_fuera['negras'], 0)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_ayuda(self, mock_stdout):
        """Test: Mostrar ayuda funciona correctamente"""
        self.cli.mostrar_ayuda()
        output = mock_stdout.getvalue()
        
        # Verificar que contiene elementos esperados de la ayuda
        self.assertIn("COMANDOS DISPONIBLES", output)
        self.assertIn("help, h", output)
        self.assertIn("dados, d", output)
        self.assertIn("LEYENDA DEL TABLERO", output)
        self.assertIn("B = Fichas Blancas", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_estado(self, mock_stdout):
        """Test: Mostrar estado del juego"""
        self.cli.mostrar_estado()
        output = mock_stdout.getvalue()
        
        # Verificar elementos del estado
        self.assertIn("ESTADO RESUMIDO", output)
        self.assertIn("Turno: Blancas", output)
        self.assertIn("Sin dados pendientes", output)
        self.assertIn("Fichas fuera - Blancas: 0, Negras: 0", output)

if __name__ == "__main__":
    unittest.main()