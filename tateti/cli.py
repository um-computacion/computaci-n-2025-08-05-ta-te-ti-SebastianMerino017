
import os
import sys
from .tateti import Tateti, JuegoTerminadoException
from .tablero import PosOcupadaException, PosInvalidaException
from .jugadores import GestorJugadores


class CLI:
    
    def __init__(self):
        """Inicializa la interfaz CLI"""
        self.juego = Tateti()
        self.gestor_jugadores = GestorJugadores()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del juego"""
        print("=" * 50)
        print("JUEGO DE TATETI (TRES EN LÍNEA)")
        print("=" * 50)
        print("1. Nuevo Juego")
        print("2. Ver Estadísticas") 
        print("3. Cómo Jugar")
        print("4. Reiniciar Estadísticas")
        print("5. Salir")
        print("=" * 50)
    
    def obtener_nombres_jugadores(self):
        print("\nCONFIGURACIÓN DE JUGADORES")
        print("-" * 30)
        
        nombre_x = input("Nombre del jugador X: ").strip()
        if not nombre_x:
            nombre_x = "Jugador X"
        
        nombre_o = input("Nombre del jugador O: ").strip()  
        if not nombre_o:
            nombre_o = "Jugador O"
        
        return nombre_x, nombre_o
    
    def solicitar_jugada(self):
        try:
            estado = self.juego.obtener_estado_juego()
            jugador_actual = self.gestor_jugadores.obtener_nombre_por_ficha(estado['turno_actual'])
            
            print(f"\n Turno de {jugador_actual} ({estado['turno_actual']})")
            print(f"Posiciones libres: {len(estado['posiciones_libres'])}")
            
            entrada = input("Ingrese fila y columna (ej: 0 1) o 'q' para volver al menú: ").strip().lower()
            
            if entrada == 'q':
                return None, None
            
            # Intentar parsear la entrada
            partes = entrada.split()
            if len(partes) != 2:
                print("⚠️ Formato inválido. Use: fila columna (ej: 0 1)")
                return -1, -1  # Código de error
            
            fila = int(partes[0])
            columna = int(partes[1])
            
            return fila, columna
        
        except ValueError:
            print("⚠️ Por favor, ingrese números válidos.")
            return -1, -1
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return -1, -1
    
    def mostrar_estado_juego(self):
        """Muestra el estado actual del juego"""
        estado = self.juego.obtener_estado_juego()
        
        print(f"\n{self.juego.obtener_mensaje_estado()}")
        print("Tablero actual:")
        self.juego.tablero.mostrar_tablero()
        
        if not estado['juego_terminado']:
            print(f"Posiciones libres: {estado['posiciones_libres']}")
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas de los jugadores"""
        if not self.gestor_jugadores.jugadores_configurados():
            print("\n No hay estadísticas disponibles. ¡Juega una partida primero!")
            return
        
        stats = self.gestor_jugadores.obtener_estadisticas_generales()
        
        print("\n" + "=" * 50)
        print("ESTADÍSTICAS DE LA SESIÓN")
        print("=" * 50)
        
        # Estadísticas individuales
        print(f" {stats['jugador_x']['nombre']} (X):")
        print(f"   Victorias: {stats['jugador_x']['victorias']}")
        print(f"   Porcentaje: {stats['jugador_x']['porcentaje_victorias']}%")
        
        print(f"\n {stats['jugador_o']['nombre']} (O):")
        print(f"   Victorias: {stats['jugador_o']['victorias']}")
        print(f"   Porcentaje: {stats['jugador_o']['porcentaje_victorias']}%")
        
        # Estadísticas generales
        print(f"\n RESUMEN GENERAL:")
        print(f"   Total de partidas: {stats['total_partidas']}")
        print(f"   Empates: {stats['empates']}")
        
        print("=" * 50)
    
    def mostrar_ayuda(self):
        print("\n" + "=" * 50)
        print("CÓMO JUGAR TATETI")
        print("=" * 50)
        print("Objetivo: Ser el primero en conseguir 3 fichas en línea")
        print("Coordenadas: Fila y columna van de 0 a 2")
        print("Turnos: Los jugadores alternan turnos (X empieza)")
        print("Victoria: 3 fichas en línea (horizontal, vertical o diagonal)")
        print("Empate: Tablero lleno sin ganador")
        print("\nEjemplo de entrada: '1 2' (fila 1, columna 2)")
        
        # Mostrar tablero de ejemplo con coordenadas
        self.juego.tablero.mostrar_posiciones_numeradas()
        
        print("=" * 50)
    
    def preguntar_continuar(self):
        respuesta = input("\n¿Jugar otra partida? (s/n): ").strip().lower()
        return respuesta in ['s', 'si', 'sí', 'y', 'yes']
    
    def ejecutar_partida(self):
        # Configurar jugadores si no están configurados
        if not self.gestor_jugadores.jugadores_configurados():
            nombre_x, nombre_o = self.obtener_nombres_jugadores()
            self.gestor_jugadores.configurar_jugadores(nombre_x, nombre_o)
        
        while True:
            # Reiniciar juego
            self.limpiar_pantalla()
            self.juego.reiniciar_juego()
            
            print("🎮 ¡Nueva partida iniciada!")
            self.mostrar_estado_juego()
            
            # Loop principal del juego
            while not self.juego.juego_terminado:
                fila, columna = self.solicitar_jugada()
                
                # Verificar si quiere salir
                if fila is None and columna is None:
                    return
                
                # Verificar entrada inválida
                if fila == -1 or columna == -1:
                    input("Presiona Enter para continuar...")
                    continue
                
                try:
                    # Intentar realizar la jugada
                    self.juego.ocupar_una_de_las_casillas(fila, columna)
                    
                    # Limpiar pantalla y mostrar estado actualizado
                    self.limpiar_pantalla()
                    self.mostrar_estado_juego()
                    
                except (PosOcupadaException, PosInvalidaException, JuegoTerminadoException) as e:
                    print(f"⚠️ Error: {e}")
                    input("Presiona Enter para continuar...")
                except Exception as e:
                    print(f"💥 Error inesperado: {e}")
                    input("Presiona Enter para continuar...")
            
            # Registrar resultado de la partida
            estado = self.juego.obtener_estado_juego()
            self.gestor_jugadores.registrar_resultado_partida(
                ganador=estado['ganador'], 
                empate=estado['empate']
            )
            
            # Mostrar estadísticas después de cada partida
            self.mostrar_estadisticas()
            
            # Preguntar si quiere continuar
            if not self.preguntar_continuar():
                break
    
    def ejecutar_juego(self):
     """Ejecuta el loop principal del juego""" 