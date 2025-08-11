import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tateti.jugadores import Jugador, GestorJugadores

class TestJugador(unittest.TestCase):
    
    def setUp(self):
        self.jugador = Jugador("Ana", "X")
    
    def test_inicializacion_jugador(self):
        self.assertEqual(self.jugador.nombre, "Ana")
        self.assertEqual(self.jugador.ficha, "X")
        self.assertEqual(self.jugador.victorias, 0)
        self.assertEqual(self.jugador.partidas_jugadas, 0)
    
    def test_incrementar_victoria(self):
        self.jugador.incrementar_victoria()
        self.assertEqual(self.jugador.victorias, 1)
        
        self.jugador.incrementar_victoria()
        self.assertEqual(self.jugador.victorias, 2)
    
    def test_incrementar_partida(self):
        self.jugador.incrementar_partida()
        self.assertEqual(self.jugador.partidas_jugadas, 1)
        
        self.jugador.incrementar_partida()
        self.assertEqual(self.jugador.partidas_jugadas, 2)
    
    def test_obtener_estadisticas_sin_partidas(self):
        stats = self.jugador.obtener_estadisticas()
        
        expected = {
            'nombre': 'Ana',
            'ficha': 'X',
            'victorias': 0,
            'derrotas': 0,
            'partidas_jugadas': 0,
            'porcentaje_victorias': 0
        }
        
        self.assertEqual(stats, expected)
    
    def test_obtener_estadisticas_con_partidas(self):
        for _ in range(3):
            self.jugador.incrementar_partida()
        
        for _ in range(2):
            self.jugador.incrementar_victoria()
        
        stats = self.jugador.obtener_estadisticas()
        
        self.assertEqual(stats['victorias'], 2)
        self.assertEqual(stats['derrotas'], 1)
        self.assertEqual(stats['partidas_jugadas'], 3)
        self.assertAlmostEqual(stats['porcentaje_victorias'], 66.7, places=1)
    
    def test_reiniciar_estadisticas(self):
        self.jugador.incrementar_partida()
        self.jugador.incrementar_victoria()
        
        self.jugador.reiniciar_estadisticas()
        
        self.assertEqual(self.jugador.victorias, 0)
        self.assertEqual(self.jugador.partidas_jugadas, 0)
    
    def test_str_representation(self):
        expected = "Ana (X)"
        self.assertEqual(str(self.jugador), expected)
    
    def test_repr_representation(self):
        expected = "Jugador(nombre='Ana', ficha='X', victorias=0)"
        self.assertEqual(repr(self.jugador), expected)

class TestGestorJugadores(unittest.TestCase):
    
    def setUp(self):
        self.gestor = GestorJugadores()
    
    def test_inicializacion_gestor(self):
        self.assertIsNone(self.gestor.jugador_x)
        self.assertIsNone(self.gestor.jugador_o)
        self.assertEqual(len(self.gestor.historial_partidas), 0)
    
    def test_configurar_jugadores(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.assertEqual(self.gestor.jugador_x.nombre, "Ana")
        self.assertEqual(self.gestor.jugador_x.ficha, "X")
        self.assertEqual(self.gestor.jugador_o.nombre, "Carlos")
        self.assertEqual(self.gestor.jugador_o.ficha, "O")
    
    def test_obtener_jugador_por_ficha(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        jugador_x = self.gestor.obtener_jugador_por_ficha("X")
        jugador_o = self.gestor.obtener_jugador_por_ficha("O")
        jugador_invalido = self.gestor.obtener_jugador_por_ficha("Z")
        
        self.assertEqual(jugador_x.nombre, "Ana")
        self.assertEqual(jugador_o.nombre, "Carlos")
        self.assertIsNone(jugador_invalido)
    
    def test_jugadores_configurados(self):
        self.assertFalse(self.gestor.jugadores_configurados())
        
        self.gestor.configurar_jugadores("Ana", "Carlos")
        self.assertTrue(self.gestor.jugadores_configurados())
    
    def test_registrar_resultado_victoria_x(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador="X", empate=False)
        
        self.assertEqual(self.gestor.jugador_x.victorias, 1)
        self.assertEqual(self.gestor.jugador_o.victorias, 0)
        self.assertEqual(self.gestor.jugador_x.partidas_jugadas, 1)
        self.assertEqual(self.gestor.jugador_o.partidas_jugadas, 1)
        self.assertEqual(len(self.gestor.historial_partidas), 1)
    
    def test_registrar_resultado_victoria_o(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador="O", empate=False)
        
        self.assertEqual(self.gestor.jugador_x.victorias, 0)
        self.assertEqual(self.gestor.jugador_o.victorias, 1)
        self.assertEqual(self.gestor.jugador_x.partidas_jugadas, 1)
        self.assertEqual(self.gestor.jugador_o.partidas_jugadas, 1)
    
    def test_registrar_resultado_empate(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador=None, empate=True)
        
        self.assertEqual(self.gestor.jugador_x.victorias, 0)
        self.assertEqual(self.gestor.jugador_o.victorias, 0)
        self.assertEqual(self.gestor.jugador_x.partidas_jugadas, 1)
        self.assertEqual(self.gestor.jugador_o.partidas_jugadas, 1)
        
        resultado = self.gestor.historial_partidas[0]
        self.assertTrue(resultado['empate'])
        self.assertIsNone(resultado['ganador'])
    
    def test_registrar_resultado_sin_configurar(self):
        self.gestor.registrar_resultado_partida(ganador="X", empate=False)
        self.assertEqual(len(self.gestor.historial_partidas), 0)
    
    def test_obtener_estadisticas_generales(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador="X", empate=False)
        self.gestor.registrar_resultado_partida(ganador="O", empate=False)
        self.gestor.registrar_resultado_partida(ganador=None, empate=True)
        
        stats = self.gestor.obtener_estadisticas_generales()
        
        self.assertEqual(stats['jugador_x']['victorias'], 1)
        self.assertEqual(stats['jugador_o']['victorias'], 1)
        self.assertEqual(stats['total_partidas'], 3)
        self.assertEqual(stats['empates'], 1)
        self.assertEqual(len(stats['historial']), 3)
    
    def test_obtener_estadisticas_sin_configurar(self):
        stats = self.gestor.obtener_estadisticas_generales()
        self.assertEqual(stats, {})
    
    def test_obtener_nombre_por_ficha(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.assertEqual(self.gestor.obtener_nombre_por_ficha("X"), "Ana")
        self.assertEqual(self.gestor.obtener_nombre_por_ficha("O"), "Carlos")
        self.assertIsNone(self.gestor.obtener_nombre_por_ficha("Z"))
    
    def test_reiniciar_estadisticas(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador="X", empate=False)
        self.gestor.registrar_resultado_partida(ganador="O", empate=False)
        
        self.gestor.reiniciar_estadisticas()
        
        self.assertEqual(self.gestor.jugador_x.victorias, 0)
        self.assertEqual(self.gestor.jugador_o.victorias, 0)
        self.assertEqual(self.gestor.jugador_x.partidas_jugadas, 0)
        self.assertEqual(self.gestor.jugador_o.partidas_jugadas, 0)
        self.assertEqual(len(self.gestor.historial_partidas), 0)
    
    def test_intercambiar_fichas(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador="X", empate=False)
        self.gestor.registrar_resultado_partida(ganador="O", empate=False)
        
        self.gestor.intercambiar_fichas()
        
        self.assertEqual(self.gestor.jugador_x.nombre, "Carlos")
        self.assertEqual(self.gestor.jugador_o.nombre, "Ana")
        
        self.assertEqual(self.gestor.jugador_x.victorias, 1)
        self.assertEqual(self.gestor.jugador_o.victorias, 1)
    
    def test_intercambiar_fichas_sin_configurar(self):
        self.gestor.intercambiar_fichas()
        self.assertIsNone(self.gestor.jugador_x)
        self.assertIsNone(self.gestor.jugador_o)
    
    def test_historial_partidas_detallado(self):
        self.gestor.configurar_jugadores("Ana", "Carlos")
        
        self.gestor.registrar_resultado_partida(ganador="X", empate=False)
        self.gestor.registrar_resultado_partida(ganador="O", empate=False)
        self.gestor.registrar_resultado_partida(ganador=None, empate=True)
        
        historial = self.gestor.historial_partidas
        
        self.assertEqual(len(historial), 3)
        
        self.assertEqual(historial[0]['jugador_x'], "Ana")
        self.assertEqual(historial[0]['jugador_o'], "Carlos")
        self.assertEqual(historial[0]['ganador'], "X")
        self.assertFalse(historial[0]['empate'])
        
        self.assertEqual(historial[1]['ganador'], "O")
        self.assertFalse(historial[1]['empate'])
        
        self.assertIsNone(historial[2]['ganador'])
        self.assertTrue(historial[2]['empate'])

if __name__ == '__main__':
    unittest.main()