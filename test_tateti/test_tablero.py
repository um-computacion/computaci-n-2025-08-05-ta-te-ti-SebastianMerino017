import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tateti.tablero import Tablero, PosOcupadaException

class TestTablero(unittest.TestCase):
    
    def setUp(self):
        self.tablero = Tablero()
    
    def test_tablero_vacio_inicialmente(self):
        for fila in self.tablero.contenedor:
            for casilla in fila:
                self.assertEqual(casilla, "")
    
    def test_poner_ficha_en_posicion_libre(self):
        self.tablero.poner_la_ficha(0, 0, "X")
        self.assertEqual(self.tablero.contenedor[0][0], "X")
    
    def test_poner_ficha_en_posicion_ocupada(self):
        self.tablero.poner_la_ficha(0, 0, "X")
        with self.assertRaises(PosOcupadaException):
            self.tablero.poner_la_ficha(0, 0, "O")
    
    def test_hay_ganador_fila(self):
        self.tablero.contenedor[0] = ["X", "X", "X"]
        self.assertEqual(self.tablero.hay_ganador(), "X")
    
    def test_hay_ganador_columna(self):
        for i in range(3):
            self.tablero.contenedor[i][0] = "O"
        self.assertEqual(self.tablero.hay_ganador(), "O")
    
    def test_hay_ganador_diagonal_principal(self):
        for i in range(3):
            self.tablero.contenedor[i][i] = "X"
        self.assertEqual(self.tablero.hay_ganador(), "X")
    
    def test_hay_ganador_diagonal_secundaria(self):
        self.tablero.contenedor[0][2] = "O"
        self.tablero.contenedor[1][1] = "O"
        self.tablero.contenedor[2][0] = "O"
        self.assertEqual(self.tablero.hay_ganador(), "O")
    
    def test_no_hay_ganador(self):
        self.tablero.contenedor[0] = ["X", "O", "X"]
        self.tablero.contenedor[1] = ["O", "X", "O"]
        self.tablero.contenedor[2] = ["O", "X", ""]
        self.assertIsNone(self.tablero.hay_ganador())
    
    def test_tablero_lleno(self):
        for i in range(3):
            for j in range(3):
                self.tablero.contenedor[i][j] = "X" if (i + j) % 2 == 0 else "O"
        self.assertTrue(self.tablero.esta_lleno())
    
    def test_tablero_no_lleno(self):
        self.tablero.contenedor[0][0] = "X"
        self.assertFalse(self.tablero.esta_lleno())


if __name__ == '__main__':
    unittest.main()