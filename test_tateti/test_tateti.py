import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tateti.tateti import Tateti
from tateti.tablero import PosOcupadaException

class TestTateti(unittest.TestCase):
    
    def setUp(self):
        self.juego = Tateti("Ana", "Carlos")
    
    def test_juego_inicializa_correctamente(self):
        self.assertEqual(self.juego.turno, "X")
        self.assertFalse(self.juego.terminado)
        self.assertIsNone(self.juego.ganador)
        self.assertEqual(self.juego.jugadores.jugador_x["nombre"], "Ana")
        self.assertEqual(self.juego.jugadores.jugador_o["nombre"], "Carlos")
    
    def test_ocupar_casilla_cambia_turno(self):
        self.juego.ocupar_una_de_las_casillas(0, 0)
        self.assertEqual(self.juego.turno, "0")
        
        self.juego.ocupar_una_de_las_casillas(0, 1)
        self.assertEqual(self.juego.turno, "X")
    
    def test_obtener_nombre_turno_actual(self):
        self.assertEqual(self.juego.obtener_nombre_turno_actual(), "Ana")
        self.juego.ocupar_una_de_las_casillas(0, 0)
        self.assertEqual(self.juego.obtener_nombre_turno_actual(), "Carlos")
    
    def test_ocupar_casilla_ocupada_no_cambia_turno(self):
        self.juego.ocupar_una_de_las_casillas(0, 0)
        turno_antes = self.juego.turno
        
        with self.assertRaises(PosOcupadaException):
            self.juego.ocupar_una_de_las_casillas(0, 0)
        
        self.assertEqual(self.juego.turno, turno_antes)
    
    def test_detectar_victoria_x(self):
        self.juego.ocupar_una_de_las_casillas(0, 0)
        self.juego.ocupar_una_de_las_casillas(1, 0)
        self.juego.ocupar_una_de_las_casillas(0, 1)
        self.juego.ocupar_una_de_las_casillas(1, 1)
        self.juego.ocupar_una_de_las_casillas(0, 2)
        
        self.assertTrue(self.juego.terminado)
        self.assertEqual(self.juego.ganador, "X")
        self.assertIn("Ana", self.juego.obtener_estado())
    
    def test_detectar_empate(self):
        jugadas = [
            (0, 0), (0, 1), (0, 2),
            (1, 1), (1, 0), (1, 2),
            (2, 1), (2, 0), (2, 2)
        ]
        
        for fila, col in jugadas:
            if not self.juego.terminado:
                self.juego.ocupar_una_de_las_casillas(fila, col)
        
        self.assertTrue(self.juego.terminado)
        self.assertIsNone(self.juego.ganador)
        self.assertEqual(self.juego.obtener_estado(), "Empate")
    
    def test_no_permitir_jugada_despues_de_terminar(self):
        self.juego.ocupar_una_de_las_casillas(0, 0)
        self.juego.ocupar_una_de_las_casillas(1, 0)
        self.juego.ocupar_una_de_las_casillas(0, 1)
        self.juego.ocupar_una_de_las_casillas(1, 1)
        self.juego.ocupar_una_de_las_casillas(0, 2)
        
        with self.assertRaises(Exception):
            self.juego.ocupar_una_de_las_casillas(2, 2)

if __name__ == '__main__':
    unittest.main()