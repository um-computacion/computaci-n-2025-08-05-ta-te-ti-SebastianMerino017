import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tateti.cli import CLI
from tateti.tateti import JuegoTerminadoException
from tateti.tablero import PosOcupadaException, PosInvalidaException

class TestCLI(unittest.TestCase):
    
    def setUp(self):
        self.cli = CLI()
    
    def test_inicializacion(self):
        self.assertIsNotNone(self.cli.juego)
        self.assertIsNotNone(self.cli.gestor_jugadores)
        self.assertEqual(self.cli.juego.turno, "X")
        self.assertFalse(self.cli.juego.juego_terminado)
    
    def test_juego_inicial_estado(self):
        estado = self.cli.juego.obtener_estado_juego()
        self.assertEqual(estado['turno_actual'], 'X')
        self.assertFalse(estado['juego_terminado'])
        self.assertIsNone(estado['ganador'])
        self.assertFalse(estado['empate'])
        self.assertEqual(len(estado['posiciones_libres']), 9)
    
    def test_gestor_jugadores_inicial(self):
        self.assertFalse(self.cli.gestor_jugadores.jugadores_configurados())
        self.assertIsNone(self.cli.gestor_jugadores.jugador_x)
        self.assertIsNone(self.cli.gestor_jugadores.jugador_o)
    
    def test_configurar_jugadores_manualmente(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        self.assertTrue(self.cli.gestor_jugadores.jugadores_configurados())
        self.assertEqual(self.cli.gestor_jugadores.jugador_x.nombre, "Ana")
        self.assertEqual(self.cli.gestor_jugadores.jugador_o.nombre, "Carlos")
    
    def test_realizar_jugadas_programaticamente(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Simular jugadas directamente en el juego
        self.cli.juego.ocupar_una_de_las_casillas(0, 0)  # X
        self.assertEqual(self.cli.juego.turno, "O")
        
        self.cli.juego.ocupar_una_de_las_casillas(1, 1)  # O
        self.assertEqual(self.cli.juego.turno, "X")
        
        self.cli.juego.ocupar_una_de_las_casillas(0, 1)  # X
        self.assertEqual(self.cli.juego.turno, "O")
    
    def test_detectar_victoria_horizontal(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Crear victoria horizontal para X
        self.cli.juego.ocupar_una_de_las_casillas(0, 0)  # X
        self.cli.juego.ocupar_una_de_las_casillas(1, 0)  # O
        self.cli.juego.ocupar_una_de_las_casillas(0, 1)  # X
        self.cli.juego.ocupar_una_de_las_casillas(1, 1)  # O
        self.cli.juego.ocupar_una_de_las_casillas(0, 2)  # X gana
        
        self.assertTrue(self.cli.juego.juego_terminado)
        self.assertEqual(self.cli.juego.ganador, "X")
    
    def test_detectar_empate(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Crear un empate
        movimientos = [
            (0, 0), (0, 1), (0, 2),  # X, O, X
            (1, 1), (1, 0), (1, 2),  # O, X, O
            (2, 1), (2, 0), (2, 2)   # X, O, X
        ]
        
        for fila, columna in movimientos:
            if not self.cli.juego.juego_terminado:
                self.cli.juego.ocupar_una_de_las_casillas(fila, columna)
        
        self.assertTrue(self.cli.juego.juego_terminado)
        self.assertTrue(self.cli.juego.empate)
        self.assertIsNone(self.cli.juego.ganador)
    
    def test_registrar_estadisticas_victoria(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Registrar una victoria para X
        self.cli.gestor_jugadores.registrar_resultado_partida("X", False)
        
        stats = self.cli.gestor_jugadores.obtener_estadisticas_generales()
        self.assertEqual(stats['jugador_x']['victorias'], 1)
        self.assertEqual(stats['jugador_o']['victorias'], 0)
        self.assertEqual(stats['total_partidas'], 1)
        self.assertEqual(stats['empates'], 0)
    
    def test_registrar_estadisticas_empate(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Registrar un empate
        self.cli.gestor_jugadores.registrar_resultado_partida(None, True)
        
        stats = self.cli.gestor_jugadores.obtener_estadisticas_generales()
        self.assertEqual(stats['jugador_x']['victorias'], 0)
        self.assertEqual(stats['jugador_o']['victorias'], 0)
        self.assertEqual(stats['total_partidas'], 1)
        self.assertEqual(stats['empates'], 1)
    
    def test_reiniciar_juego(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Hacer algunas jugadas
        self.cli.juego.ocupar_una_de_las_casillas(0, 0)
        self.cli.juego.ocupar_una_de_las_casillas(1, 1)
        
        # Reiniciar
        self.cli.juego.reiniciar_juego()
        
        # Verificar estado inicial
        self.assertEqual(self.cli.juego.turno, "X")
        self.assertFalse(self.cli.juego.juego_terminado)
        self.assertIsNone(self.cli.juego.ganador)
        
        # Verificar tablero vacío
        for fila in self.cli.juego.tablero.contenedor:
            for casilla in fila:
                self.assertEqual(casilla, "")
    
    def test_obtener_nombre_por_ficha(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        nombre_x = self.cli.gestor_jugadores.obtener_nombre_por_ficha("X")
        nombre_o = self.cli.gestor_jugadores.obtener_nombre_por_ficha("O")
        nombre_invalido = self.cli.gestor_jugadores.obtener_nombre_por_ficha("Z")
        
        self.assertEqual(nombre_x, "Ana")
        self.assertEqual(nombre_o, "Carlos")
        self.assertIsNone(nombre_invalido)
    
    def test_manejo_excepciones_posicion_ocupada(self):
        self.cli.juego.ocupar_una_de_las_casillas(0, 0)
        
        with self.assertRaises(PosOcupadaException):
            self.cli.juego.ocupar_una_de_las_casillas(0, 0)
    
    def test_manejo_excepciones_posicion_invalida(self):
        with self.assertRaises(PosInvalidaException):
            self.cli.juego.ocupar_una_de_las_casillas(-1, 0)
        
        with self.assertRaises(PosInvalidaException):
            self.cli.juego.ocupar_una_de_las_casillas(3, 0)
    
    def test_manejo_excepciones_juego_terminado(self):
        # Crear victoria rápida
        self.cli.juego.ocupar_una_de_las_casillas(0, 0)  # X
        self.cli.juego.ocupar_una_de_las_casillas(1, 0)  # O
        self.cli.juego.ocupar_una_de_las_casillas(0, 1)  # X
        self.cli.juego.ocupar_una_de_las_casillas(1, 1)  # O
        self.cli.juego.ocupar_una_de_las_casillas(0, 2)  # X gana
        
        with self.assertRaises(JuegoTerminadoException):
            self.cli.juego.ocupar_una_de_las_casillas(2, 2)
    
    def test_intercambio_fichas(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Registrar algunas estadísticas
        self.cli.gestor_jugadores.registrar_resultado_partida("X", False)  # Ana gana
        self.cli.gestor_jugadores.registrar_resultado_partida("O", False)  # Carlos gana
        
        # Intercambiar fichas
        self.cli.gestor_jugadores.intercambiar_fichas()
        
        # Verificar intercambio
        self.assertEqual(self.cli.gestor_jugadores.jugador_x.nombre, "Carlos")
        self.assertEqual(self.cli.gestor_jugadores.jugador_o.nombre, "Ana")
        
        # Verificar que las estadísticas se mantuvieron
        self.assertEqual(self.cli.gestor_jugadores.jugador_x.victorias, 1)  # Carlos
        self.assertEqual(self.cli.gestor_jugadores.jugador_o.victorias, 1)  # Ana
    
    def test_multiples_partidas(self):
        self.cli.gestor_jugadores.configurar_jugadores("Ana", "Carlos")
        
        # Simular múltiples partidas
        for i in range(3):
            # Reiniciar juego para nueva partida
            self.cli.juego.reiniciar_juego()
            
            # Simular una partida con victoria alternada
            if i % 2 == 0:
                # Ana (X) gana
                self.cli.juego.ocupar_una_de_las_casillas(0, 0)  # X
                self.cli.juego.ocupar_una_de_las_casillas(1, 0)  # O
                self.cli.juego.ocupar_una_de_las_casillas(0, 1)  # X
                self.cli.juego.ocupar_una_de_las_casillas(1, 1)  # O
                self.cli.juego.ocupar_una_de_las_casillas(0, 2)  # X gana
                
                # Registrar resultado
                estado = self.cli.juego.obtener_estado_juego()
                self.cli.gestor_jugadores.registrar_resultado_partida(
                    estado['ganador'], estado['empate']
                )
            else:
                # Carlos (O) gana
                self.cli.juego.ocupar_una_de_las_casillas(0, 0)  # X
                self.cli.juego.ocupar_una_de_las_casillas(1, 0)  # O
                self.cli.juego.ocupar_una_de_las_casillas(0, 1)  # X
                self.cli.juego.ocupar_una_de_las_casillas(1, 1)  # O
                self.cli.juego.ocupar_una_de_las_casillas(2, 2)  # X
                self.cli.juego.ocupar_una_de_las_casillas(1, 2)  # O gana
                
                # Registrar resultado
                estado = self.cli.juego.obtener_estado_juego()
                self.cli.gestor_jugadores.registrar_resultado_partida(
                    estado['ganador'], estado['empate']
                )
        
        # Verificar estadísticas finales
        stats = self.cli.gestor_jugadores.obtener_estadisticas_generales()
        self.assertEqual(stats['total_partidas'], 3)
        self.assertEqual(stats['jugador_x']['victorias'], 2)  # Ana ganó 2 veces
        self.assertEqual(stats['jugador_o']['victorias'], 1)  # Carlos ganó 1 vez

if __name__ == '__main__':
    unittest.main()