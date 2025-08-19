import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tateti.jugador import Jugador

class TestJugador(unittest.TestCase):
    
    def test_crear_jugadores_con_nombres_por_defecto(self):
        jugador = Jugador()
        self.assertEqual(jugador.jugador_x["nombre"], "Jugador 1")
        self.assertEqual(jugador.jugador_x["simbolo"], "X")
        self.assertEqual(jugador.jugador_o["nombre"], "Jugador 2")
        self.assertEqual(jugador.jugador_o["simbolo"], "0")
    
    def test_crear_jugadores_con_nombres_personalizados(self):
        jugador = Jugador("Ana", "Carlos")
        self.assertEqual(jugador.jugador_x["nombre"], "Ana")
        self.assertEqual(jugador.jugador_o["nombre"], "Carlos")
    
    def test_obtener_jugador_por_simbolo(self):
        jugador = Jugador("Ana", "Carlos")
        jugador_x = jugador.obtener_jugador_por_simbolo("X")
        jugador_o = jugador.obtener_jugador_por_simbolo("0")
        
        self.assertEqual(jugador_x["nombre"], "Ana")
        self.assertEqual(jugador_o["nombre"], "Carlos")
        self.assertIsNone(jugador.obtener_jugador_por_simbolo("Z"))
    
    def test_obtener_nombre_por_simbolo(self):
        jugador = Jugador("Ana", "Carlos")
        self.assertEqual(jugador.obtener_nombre_por_simbolo("X"), "Ana")
        self.assertEqual(jugador.obtener_nombre_por_simbolo("0"), "Carlos")
        self.assertIsNone(jugador.obtener_nombre_por_simbolo("Z"))
    
    def test_str_jugadores(self):
        jugador = Jugador("Ana", "Carlos")
        self.assertEqual(str(jugador), "Ana (X) vs Carlos (0)")

if __name__ == '__main__':
    unittest.main()