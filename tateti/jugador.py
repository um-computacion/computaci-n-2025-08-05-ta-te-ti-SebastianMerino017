class Jugador:
    def __init__(self, nombre1="Jugador 1", nombre2="Jugador 2"):
        self.jugador_x = {"nombre": nombre1, "simbolo": "X"}
        self.jugador_o = {"nombre": nombre2, "simbolo": "0"}
        self.jugadores = [self.jugador_x, self.jugador_o]
    
    def obtener_jugador_por_simbolo(self, simbolo):
        if simbolo == "X":
            return self.jugador_x
        elif simbolo == "0":
            return self.jugador_o
        return None
    
    def obtener_nombre_por_simbolo(self, simbolo):
        jugador = self.obtener_jugador_por_simbolo(simbolo)
        return jugador["nombre"] if jugador else None
    
    def __str__(self):
        return f"{self.jugador_x['nombre']} (X) vs {self.jugador_o['nombre']} (0)"