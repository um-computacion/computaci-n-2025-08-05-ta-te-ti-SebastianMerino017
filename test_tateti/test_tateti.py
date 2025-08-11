import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tateti.tateti import Tateti, JuegoTerminadoException
from tateti.tablero import PosOcupadaException, PosInvalidaException

class TestTateti(unittest.TestCase):
    
    def setUp(self):
        self.juego = Tateti()
    
    def test_inicializacion(self):
        self.assertEqual(self.juego.turno, "X")
        self.assertIsNone(self.juego.ganador)
        self.assertFalse(self.juego.juego_terminado)
        self.assertFalse(self.juego.empate)
        
        for fila in self.juego.tablero.contenedor:
            for casilla in fila:
                self.assertEqual(casilla, "")
    
    def test_ocupar_casilla_valida(self):
        self.juego.ocupar_una_de_las_casillas(1, 1)
        
        self.assertEqual(self.juego.tablero.contenedor[1][1], "X")
        
        self.assertEqual(self.juego.turno, "O")
    
    def test_ocupar_casilla_posicion_ocupada(self):
        self.juego.ocupar_una_de_las_casillas(0, 0)
        
        with self.assertRaises(PosOcupadaException):
            self.juego.ocupar_una_de_las_casillas(0, 0)
    
    def test_ocupar_casilla_posicion_invalida(self):
        with self.assertRaises(PosInvalidaException):
            self.juego.ocupar_una_de_las_casillas(-1, 0)
    
    def test_ocupar_casilla_juego_terminado(self):
        self.juego.ocupar_una_de_las_casillas(0, 0)
        self.juego.ocupar_una_de_las_casillas(1, 0)
        self.juego.ocupar_una_de_las_casillas(0, 1)
        self.juego.ocupar_una_de_las_casillas(1, 1)
        self.juego.ocupar_una_de_las_casillas(0, 2)
        
        with self.assertRaises(JuegoTerminadoException):
            self.juego.ocupar_una_de_las_casillas(2, 2)

if __name__ == '__main__':
    unittest.main()