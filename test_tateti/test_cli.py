import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tateti.cli import CLI

class TestCLI(unittest.TestCase):
    
    @patch('builtins.input', side_effect=['Ana', 'Carlos'])
    def setUp(self, mock_input):
        with patch('builtins.print'):
            self.cli = CLI()
    
    def test_crear_cli(self):
        self.assertIsNotNone(self.cli.juego)
        self.assertEqual(self.cli.juego.turno, "X")
        self.assertEqual(self.cli.juego.jugadores.jugador_x["nombre"], "Ana")
        self.assertEqual(self.cli.juego.jugadores.jugador_o["nombre"], "Carlos")
    
    @patch('builtins.input', side_effect=['', '', '0', '0', '1', '1', '0', '1', '1', '0', '0', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_juego_completo_con_ganador(self, mock_stdout, mock_input):
        with patch('builtins.print'):
            cli = CLI()
        cli.ejecutar()
        output = mock_stdout.getvalue()
        self.assertIn("Ganador:", output)

if __name__ == '__main__':
    unittest.main()