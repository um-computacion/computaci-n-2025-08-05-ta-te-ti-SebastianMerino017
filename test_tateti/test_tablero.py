import unittest
import sys
import os
from io import StringIO

# Agregar el directorio padre al path para importar el módulo tateti
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tateti.tablero import Tablero, PosOcupadaException, PosInvalidaException


class TestTablero(unittest.TestCase):
    
    def setUp(self):
        self.tablero = Tablero()
    
    def test_inicializacion(self):
        # Verificar que el tablero se inicializa vacío
        for fila in self.tablero.contenedor:
            for casilla in fila:
                self.assertEqual(casilla, "")
        
        # Verificar dimensiones
        self.assertEqual(len(self.tablero.contenedor), 3)
        self.assertEqual(len(self.tablero.contenedor[0]), 3)
    
    def test_poner_ficha_exitosa(self):
        self.tablero.poner_la_ficha(1, 1, "X")
        self.assertEqual(self.tablero.contenedor[1][1], "X")
    
    def test_poner_ficha_posicion_ocupada(self):
        self.tablero.poner_la_ficha(0, 0, "X")
        
        with self.assertRaises(PosOcupadaException):
            self.tablero.poner_la_ficha(0, 0, "O")
    
    def test_poner_ficha_posicion_invalida(self):
        # Posiciones fuera del rango
        with self.assertRaises(PosInvalidaException):
            self.tablero.poner_la_ficha(-1, 0, "X")
        
        with self.assertRaises(PosInvalidaException):
            self.tablero.poner_la_ficha(0, 3, "X")
        
        with self.assertRaises(PosInvalidaException):
            self.tablero.poner_la_ficha(3, 0, "X")
    
    def test_esta_ocupada_posicion_libre(self):
        self.assertFalse(self.tablero.esta_ocupada(1, 1))
    
    def test_esta_ocupada_posicion_ocupada(self):
        self.tablero.poner_la_ficha(2, 2, "O")
        self.assertTrue(self.tablero.esta_ocupada(2, 2))
    
    def test_esta_ocupada_posicion_invalida(self):
        with self.assertRaises(PosInvalidaException):
            self.tablero.esta_ocupada(5, 0)
    
    def test_obtener_ficha_existente(self):
        self.tablero.poner_la_ficha(0, 2, "X")
        self.assertEqual(self.tablero.obtener_ficha(0, 2), "X")
    
    def test_obtener_ficha_vacia(self):
        self.assertEqual(self.tablero.obtener_ficha(1, 0), "")
    
    def test_obtener_ficha_posicion_invalida(self):
        with self.assertRaises(PosInvalidaException):
            self.tablero.obtener_ficha(-1, 2)
    
    def test_tablero_lleno_vacio(self):
        self.assertFalse(self.tablero.tablero_lleno())
    
    def test_tablero_lleno_parcial(self):
        self.tablero.poner_la_ficha(0, 0, "X")
        self.tablero.poner_la_ficha(1, 1, "O")
        self.assertFalse(self.tablero.tablero_lleno())
    
    def test_tablero_lleno_completo(self):
        fichas = ["X", "O", "X", "O", "X", "O", "X", "O", "X"]
        indice = 0
        
        for fil in range(3):
            for col in range(3):
                self.tablero.poner_la_ficha(fil, col, fichas[indice])
                indice += 1
        
        self.assertTrue(self.tablero.tablero_lleno())
    
    def test_obtener_posiciones_libres_tablero_vacio(self):
        posiciones = self.tablero.obtener_posiciones_libres()
        
        # Deben ser todas las 9 posiciones
        self.assertEqual(len(posiciones), 9)
        
        # Verificar que están todas las posiciones
        esperadas = [(fil, col) for fil in range(3) for col in range(3)]
        self.assertEqual(set(posiciones), set(esperadas))
    
    def test_obtener_posiciones_libres_tablero_parcial(self):
        self.tablero.poner_la_ficha(0, 0, "X")
        self.tablero.poner_la_ficha(1, 1, "O")
        self.tablero.poner_la_ficha(2, 2, "X")
        
        posiciones = self.tablero.obtener_posiciones_libres()
        
        # Deben quedar 6 posiciones libres
        self.assertEqual(len(posiciones), 6)
        
        # Verificar que las ocupadas no están en la lista
        self.assertNotIn((0, 0), posiciones)
        self.assertNotIn((1, 1), posiciones)
        self.assertNotIn((2, 2), posiciones)
    
    def test_obtener_posiciones_libres_tablero_lleno(self):
        # Llenar todo el tablero
        for fil in range(3):
            for col in range(3):
                self.tablero.poner_la_ficha(fil, col, "X")
        
        posiciones = self.tablero.obtener_posiciones_libres()
        self.assertEqual(len(posiciones), 0)
    
    def test_reiniciar_tablero(self):
        # Llenar algunas posiciones
        self.tablero.poner_la_ficha(0, 0, "X")
        self.tablero.poner_la_ficha(1, 1, "O")
        self.tablero.poner_la_ficha(2, 2, "X")
        
        # Reiniciar
        self.tablero.reiniciar()
        
        # Verificar que está vacío
        for fila in self.tablero.contenedor:
            for casilla in fila:
                self.assertEqual(casilla, "")
    
    def test_clonar_tablero(self):
        # Configurar tablero original
        self.tablero.poner_la_ficha(0, 0, "X")
        self.tablero.poner_la_ficha(1, 1, "O")
        
        # Clonar
        clon = self.tablero.clonar()
        
        # Verificar que el clon tiene el mismo estado
        self.assertEqual(clon.contenedor, self.tablero.contenedor)
        
        # Verificar que son objetos independientes
        self.assertIsNot(clon, self.tablero)
        self.assertIsNot(clon.contenedor, self.tablero.contenedor)
        
        # Verificar independencia modificando el original
        self.tablero.poner_la_ficha(2, 2, "X")
        self.assertNotEqual(clon.contenedor, self.tablero.contenedor)
    
    def test_mostrar_tablero_no_crash(self):
        # Capturar salida para verificar que no hay excepciones
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            self.tablero.mostrar_tablero()
            # Si llegamos aquí, no hubo excepción
            self.assertTrue(True)
        finally:
            sys.stdout = old_stdout
    
    def test_mostrar_posiciones_numeradas_no_crash(self):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            self.tablero.mostrar_posiciones_numeradas()
            self.assertTrue(True)
        finally:
            sys.stdout = old_stdout
    
    def test_secuencia_jugadas_completa(self):
        # Secuencia de jugadas alternadas
        jugadas = [
            (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
            (1, 0, "O"), (1, 1, "X"), (1, 2, "O"),
            (2, 0, "X"), (2, 1, "O"), (2, 2, "X")
        ]
        
        for fil, col, ficha in jugadas:
            self.tablero.poner_la_ficha(fil, col, ficha)
            self.assertEqual(self.tablero.obtener_ficha(fil, col), ficha)
        
        # Verificar que el tablero está lleno
        self.assertTrue(self.tablero.tablero_lleno())
        
        # Verificar que no hay posiciones libres
        self.assertEqual(len(self.tablero.obtener_posiciones_libres()), 0)


if __name__ == '__main__':
    unittest.main()