from .tablero import Tablero
from .jugador import Jugador

class Tateti:
    def __init__(self, nombre1="Jugador 1", nombre2="Jugador 2"):
        self.turno = "X"
        self.tablero = Tablero()
        self.jugadores = Jugador(nombre1, nombre2)
        self.terminado = False
        self.ganador = None
    
    def ocupar_una_de_las_casillas(self, fil, col):
        if self.terminado:
            raise Exception("El juego ya terminó")
        
        self.tablero.poner_la_ficha(fil, col, self.turno)
        
        ganador = self.tablero.hay_ganador()
        if ganador:
            self.ganador = ganador
            self.terminado = True
            return
        
        if self.tablero.esta_lleno():
            self.terminado = True
            return
        
        if self.turno == "X":
            self.turno = "0"
        else:
            self.turno = "X"
    
    def obtener_estado(self):
        if self.ganador:
            nombre_ganador = self.jugadores.obtener_nombre_por_simbolo(self.ganador)
            return f"Ganador: {nombre_ganador} ({self.ganador})"
        elif self.terminado:
            return "Empate"
        else:
            return "En juego"
    
    def obtener_nombre_turno_actual(self):
        return self.jugadores.obtener_nombre_por_simbolo(self.turno)