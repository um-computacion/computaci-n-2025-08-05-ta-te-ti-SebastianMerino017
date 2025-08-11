from .tablero import Tablero, PosOcupadaException, PosInvalidaException


class JuegoTerminadoException(Exception):
    pass


class Tateti:
    def __init__(self):
        self.turno = "X"  # X siempre empieza
        self.tablero = Tablero()
        self.ganador = None
        self.juego_terminado = False
        self.empate = False
    
    def ocupar_una_de_las_casillas(self, fil, col):
        if self.juego_terminado:
            raise JuegoTerminadoException("El juego ya terminó")
        
        # Poner la ficha (puede lanzar excepciones)
        self.tablero.poner_la_ficha(fil, col, self.turno)
        
        # Verificar condiciones de fin de juego
        if self.verificar_victoria(self.turno):
            self.ganador = self.turno
            self.juego_terminado = True
        elif self.tablero.tablero_lleno():
            self.empate = True
            self.juego_terminado = True
        else:
            # Cambiar turno solo si el juego continúa
            self.cambiar_turno()
    
    def cambiar_turno(self):
        if self.turno == "X":
            self.turno = "O"
        else:
            self.turno = "X"
    
    def verificar_victoria(self, ficha):
        # Verificar filas
        for fil in range(3):
            if all(self.tablero.contenedor[fil][col] == ficha for col in range(3)):
                return True
        
        # Verificar columnas
        for col in range(3):
            if all(self.tablero.contenedor[fil][col] == ficha for fil in range(3)):
                return True
        
        # Verificar diagonal principal (0,0) -> (2,2)
        if all(self.tablero.contenedor[i][i] == ficha for i in range(3)):
            return True
        
        # Verificar diagonal secundaria (0,2) -> (2,0)
        if all(self.tablero.contenedor[i][2-i] == ficha for i in range(3)):
            return True
        
        return False
    
    def obtener_estado_juego(self):
        return {
            'turno_actual': self.turno,
            'juego_terminado': self.juego_terminado,
            'ganador': self.ganador,
            'empate': self.empate,
            'tablero': self.tablero.contenedor,
            'posiciones_libres': self.tablero.obtener_posiciones_libres()
        }
    
    def reiniciar_juego(self):
        self.turno = "X"
        self.tablero.reiniciar()
        self.ganador = None
        self.juego_terminado = False
        self.empate = False
    
    def obtener_mensaje_estado(self):
        if self.juego_terminado:
            if self.empate:
                return
            else:
                return f"¡{self.ganador} ha ganado!"
        else:
            return f"Turno de {self.turno}"
    
    def es_jugada_valida(self, fil, col):
        if self.juego_terminado:
            return False
        
        try:
            return not self.tablero.esta_ocupada(fil, col)
        except PosInvalidaException:
            return False
    
    def obtener_ganador(self):
        return self.ganador
    
    def es_empate(self):
        return self.empate
    
    def obtener_combinaciones_ganadoras(self):
        combinaciones = []
        
        # Filas
        for fil in range(3):
            combinaciones.append([(fil, 0), (fil, 1), (fil, 2)])
        
        # Columnas  
        for col in range(3):
            combinaciones.append([(0, col), (1, col), (2, col)])
        
        # Diagonales
        combinaciones.append([(0, 0), (1, 1), (2, 2)])  # Principal
        combinaciones.append([(0, 2), (1, 1), (2, 0)])  # Secundaria
        
        return combinaciones