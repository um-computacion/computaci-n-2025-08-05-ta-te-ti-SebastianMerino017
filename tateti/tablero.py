class PosOcupadaException(Exception):
    ...

class Tablero:
    def __init__(self):
        self.contenedor = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
    
    def poner_la_ficha(self, fil, col, ficha):
        if self.contenedor[fil][col] == "":
            self.contenedor[fil][col] = ficha
        else:
            raise PosOcupadaException("pos ocupada!")
    
    def hay_ganador(self):
        for fila in self.contenedor:
            if fila[0] == fila[1] == fila[2] != "":
                return fila[0]
        
        for col in range(3):
            if self.contenedor[0][col] == self.contenedor[1][col] == self.contenedor[2][col] != "":
                return self.contenedor[0][col]
        
        if self.contenedor[0][0] == self.contenedor[1][1] == self.contenedor[2][2] != "":
            return self.contenedor[0][0]
        
        if self.contenedor[0][2] == self.contenedor[1][1] == self.contenedor[2][0] != "":
            return self.contenedor[0][2]
        
        return None
    
    def esta_lleno(self):
        for fila in self.contenedor:
            if "" in fila:
                return False
        return True
    
    def mostrar_tablero(self):
        print("Tablero:")
        for fila in self.contenedor:
            print(fila)