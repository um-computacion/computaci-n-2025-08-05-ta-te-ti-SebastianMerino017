from tateti.tateti import Tateti
from tateti.tablero import PosOcupadaException

class CLI:
    def __init__(self):
        print("Bienvenidos al Tateti")
        nombre1 = input("Nombre del Jugador 1 (X): ") or "Jugador 1"
        nombre2 = input("Nombre del Jugador 2 (0): ") or "Jugador 2"
        self.juego = Tateti(nombre1, nombre2)
        print(f"\n{self.juego.jugadores}\n")
    
    def ejecutar(self):
        while not self.juego.terminado:
            self.juego.tablero.mostrar_tablero()
            nombre_actual = self.juego.obtener_nombre_turno_actual()
            print(f"Turno de {nombre_actual} ({self.juego.turno}):")
            
            try:
                fila = int(input("Ingrese fila (0-2): "))
                col = int(input("Ingrese col (0-2): "))
                
                if not (0 <= fila <= 2 and 0 <= col <= 2):
                    print("Error: Fila y columna deben estar entre 0 y 2")
                    continue
                
                self.juego.ocupar_una_de_las_casillas(fila, col)
                
            except PosOcupadaException as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Ingrese números válidos")
            except Exception as e:
                print(f"Error inesperado: {e}")
        
        self.juego.tablero.mostrar_tablero()
        print(f"Juego terminado: {self.juego.obtener_estado()}")

if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()