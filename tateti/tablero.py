class PosOcupadaException(Exception):
    pass


class PosInvalidaException(Exception):
    pass


class Tablero:
    
    def __init__(self):
        self.contenedor = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
    
    def poner_la_ficha(self, fil, col, ficha):
  
        if not (0 <= fil <= 2 and 0 <= col <= 2):
            raise PosInvalidaException(f"Posición ({fil}, {col}) inválida. Debe ser entre 0-2")
        
        if self.contenedor[fil][col] == "":
            self.contenedor[fil][col] = ficha
        else:
            raise PosOcupadaException("¡Posición ocupada!")
    
    def esta_ocupada(self, fil, col):
        if not (0 <= fil <= 2 and 0 <= col <= 2):
            raise PosInvalidaException(f"Posición ({fil}, {col}) inválida. Debe ser entre 0-2")
        
        return self.contenedor[fil][col] != ""
    
    def obtener_ficha(self, fil, col):
        if not (0 <= fil <= 2 and 0 <= col <= 2):
            raise PosInvalidaException(f"Posición ({fil}, {col}) inválida. Debe ser entre 0-2")
        
        return self.contenedor[fil][col]
    
    def tablero_lleno(self):
        for fila in self.contenedor:
            for casilla in fila:
                if casilla == "":
                    return False
        return True
    
    def obtener_posiciones_libres(self):
        posiciones_libres = []
        for fil in range(3):
            for col in range(3):
                if self.contenedor[fil][col] == "":
                    posiciones_libres.append((fil, col))
        return posiciones_libres
    
    def reiniciar(self):
        self.contenedor = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
    
    def mostrar_tablero(self):
        print("\n   0   1   2")
        for i, fila in enumerate(self.contenedor):
            # Mostrar contenido de la fila con formato
            contenido_fila = []
            for casilla in fila:
                if casilla == "":
                    contenido_fila.append(" ")
                else:
                    contenido_fila.append(casilla)
            
            print(f"{i}  {contenido_fila[0]} | {contenido_fila[1]} | {contenido_fila[2]} ")
            
            # Separador entre filas (excepto en la última)
            if i < 2:
                print("  ---|---|---")
        print()
    
    def mostrar_posiciones_numeradas(self):
        print("\nPosiciones del tablero (fila, columna):")
        print("   0   1   2")
        for fil in range(3):
            contenido = []
            for col in range(3):
                contenido.append(f"({fil},{col})")
            print(f"{fil}  {contenido[0]} | {contenido[1]} | {contenido[2]} ")
            if fil < 2:
                print("  " + "-" * 25)
        print()
    
    def clonar(self):
        nuevo_tablero = Tablero()
        for fil in range(3):
            for col in range(3):
                nuevo_tablero.contenedor[fil][col] = self.contenedor[fil][col]
        return nuevo_tablero