# Tateti (Tic-Tac-Toe)

**Autor:** Sebastian Merino  
**Carrera:** Ingeniería en Informática  
**Proyecto:** Implementación del clásico juego Tateti en Python

## Descripción

Este proyecto presenta una implementación completa del juego Tateti (también conocido como Tic-Tac-Toe o Tres en Raya) desarrollado en Python. El juego incluye una interfaz de línea de comandos interactiva y está estructurado siguiendo buenas prácticas de programación orientada a objetos.

## Características

- ✅ Juego completo de Tateti para 2 jugadores
- ✅ Interfaz de línea de comandos interactiva
- ✅ Validación de movimientos y manejo de errores
- ✅ Detección automática de victoria y empates
- ✅ Nombres personalizables para los jugadores
- ✅ Suite completa de tests unitarios
- ✅ Arquitectura modular y extensible

## Estructura del Proyecto

```
tateti/
├── tateti/
│   ├── __init__.py
│   ├── cli.py          # Interfaz de línea de comandos
│   ├── tablero.py      # Lógica del tablero de juego
│   ├── jugador.py      # Gestión de jugadores
│   └── tateti.py       # Clase principal del juego
├── test_tateti/
│   ├── __init__.py
│   ├── test_cli.py     # Tests para la CLI
│   ├── test_tablero.py # Tests para el tablero
│   ├── test_jugador.py # Tests para jugadores
│   └── test_tateti.py  # Tests para el juego principal
└── README.md
```

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd tateti
```

2. Asegúrate de tener Python 3.6+ instalado:
```bash
python --version
```

## Uso

### Ejecutar el Juego

Para iniciar el juego, ejecuta:

```bash
python -m tateti.cli
```

O desde el directorio del proyecto:

```bash
python tateti/cli.py
```

### Cómo Jugar

#### Inicio del Juego
1. Ejecuta el programa y se te dará la bienvenida al Tateti
2. Ingresa el nombre del Jugador 1 (o presiona Enter para usar "Jugador 1")
3. Ingresa el nombre del Jugador 2 (o presiona Enter para usar "Jugador 2")
4. El sistema mostrará el enfrentamiento: "Nombre1 (X) vs Nombre2 (O)"

#### Durante el Juego
1. **El Jugador 1 (X) siempre comienza**
2. En cada turno verás:
   - El tablero actual
   - De quién es el turno: "Turno de [Nombre] ([Símbolo]):"
3. **Ingresa las coordenadas:**
   - Primero la fila (0, 1 o 2)
   - Luego la columna (0, 1 o 2)
4. El juego valida automáticamente tu movimiento
5. Los turnos alternan hasta que haya un ganador o empate

#### Sistema de Coordenadas
El tablero usa un sistema de coordenadas basado en índices:

```
      Columnas
      0   1   2
  0 [ ] [ ] [ ]  ← Fila 0
F 1 [ ] [ ] [ ]  ← Fila 1  
i 2 [ ] [ ] [ ]  ← Fila 2
l
a
s

Ejemplos:
- Esquina superior izquierda: fila=0, col=0
- Centro: fila=1, col=1  
- Esquina inferior derecha: fila=2, col=2
```

#### Condiciones de Victoria
El juego termina cuando:
- **Victoria**: Un jugador alinea 3 símbolos en fila, columna o diagonal
- **Empate**: Se ocupan todas las casillas sin que haya ganador

#### Manejo de Errores
El juego maneja elegantemente:
- **Posición ocupada**: "Error: pos ocupada!" 
- **Coordenadas inválidas**: "Error: Fila y columna deben estar entre 0 y 2"
- **Entrada no numérica**: "Error: Ingrese números válidos"

#### Ejemplo de Partida
```
Bienvenidos al Tateti
Nombre del Jugador 1 (X): Ana
Nombre del Jugador 2 (0): Carlos

Ana (X) vs Carlos (0)

Tablero:
['', '', '']
['', '', '']
['', '', '']
Turno de Ana (X):
Ingrese fila (0-2): 1
Ingrese col (0-2): 1

Tablero:
['', '', '']
['', 'X', '']
['', '', '']
Turno de Carlos (0):
...
```

## Arquitectura y Módulos

### `tablero.py` - Lógica del Tablero
La clase `Tablero` representa el tablero de juego de 3x3 y contiene toda la lógica relacionada con el estado del juego:

- **Inicialización**: Crea una matriz 3x3 vacía usando listas anidadas
- **Colocación de fichas**: El método `poner_la_ficha(fil, col, ficha)` valida que la posición esté libre antes de colocar una ficha
- **Detección de victoria**: `hay_ganador()` verifica todas las combinaciones ganadoras:
  - **Filas horizontales**: Revisa si alguna fila tiene 3 símbolos iguales
  - **Columnas verticales**: Verifica cada columna independientemente  
  - **Diagonal principal**: Comprueba la diagonal de esquina superior izquierda a inferior derecha
  - **Diagonal secundaria**: Verifica la diagonal de esquina superior derecha a inferior izquierda
- **Estado del tablero**: `esta_lleno()` determina si quedan casillas libres
- **Visualización**: `mostrar_tablero()` imprime el estado actual en consola
- **Manejo de errores**: `PosOcupadaException` se lanza cuando se intenta ocupar una casilla ya ocupada

### `jugador.py` - Gestión de Jugadores
La clase `Jugador` encapsula la información y gestión de ambos jugadores:

- **Estructura de datos**: Mantiene dos diccionarios con nombre y símbolo para cada jugador
- **Jugador X**: Siempre es el primer jugador y comienza el juego
- **Jugador O**: Es el segundo jugador (nota: usa "0" en lugar de "O")
- **Métodos de consulta**: 
  - `obtener_jugador_por_simbolo()`: Retorna el diccionario completo del jugador
  - `obtener_nombre_por_simbolo()`: Retorna solo el nombre del jugador
- **Representación**: El método `__str__()` muestra el enfrentamiento en formato "Jugador1 (X) vs Jugador2 (O)"

### `tateti.py` - Motor Principal del Juego
La clase `Tateti` es el coordinador principal que integra tablero y jugadores:

- **Estado del juego**: Mantiene variables para el turno actual, estado de finalización y ganador
- **Lógica de turnos**: Alterna automáticamente entre "X" y "O" después de cada jugada válida
- **Integración**: Combina las funcionalidades del tablero y jugadores
- **Control de flujo**: `ocupar_una_de_las_casillas()` ejecuta la secuencia completa:
  1. Valida que el juego no haya terminado
  2. Coloca la ficha en el tablero
  3. Verifica si hay ganador
  4. Verifica si hay empate
  5. Cambia el turno al siguiente jugador
- **Consultas de estado**: Proporciona información sobre el estado actual y el jugador en turno

### `cli.py` - Interfaz de Usuario
La clase `CLI` proporciona la interfaz de línea de comandos:

- **Inicialización interactiva**: Solicita nombres de jugadores al inicio
- **Bucle principal**: Mantiene el juego activo hasta que termine
- **Validación de entrada**: Verifica que las coordenadas estén en rango (0-2)
- **Manejo robusto de errores**: 
  - Posiciones ocupadas
  - Valores no numéricos
  - Coordenadas fuera de rango
  - Errores inesperados
- **Retroalimentación**: Muestra el tablero y mensajes informativos en cada turno

## Testing

El proyecto incluye una suite completa de tests unitarios. Para ejecutar todos los tests:

```bash
python -m unittest discover test_tateti
```

Para ejecutar tests específicos:

```bash
# Test del tablero
python -m unittest test_tateti.test_tablero

# Test de jugadores  
python -m unittest test_tateti.test_jugador

# Test del juego principal
python -m unittest test_tateti.test_tateti

# Test de la CLI
python -m unittest test_tateti.test_cli
```

### Cobertura de Tests

Los tests cubren:
- ✅ Inicialización correcta de todas las clases
- ✅ Colocación de fichas y validaciones
- ✅ Detección de victorias en filas, columnas y diagonales
- ✅ Detección de empates
- ✅ Manejo de errores y excepciones
- ✅ Cambio de turnos
- ✅ Flujo completo del juego

## Funcionamiento Interno

### Flujo de Ejecución
1. **Inicialización**: La CLI crea una instancia de `Tateti` con los nombres de los jugadores
2. **Bucle principal**: Mientras el juego no haya terminado:
   - Muestra el tablero actual
   - Solicita coordenadas al jugador en turno
   - Valida la entrada del usuario
   - Ejecuta la jugada a través de `ocupar_una_de_las_casillas()`
   - Verifica condiciones de finalización
3. **Finalización**: Muestra el resultado final (ganador o empate)

### Algoritmo de Detección de Victoria
El método `hay_ganador()` implementa un algoritmo eficiente que verifica:

1. **Filas**: Itera por cada fila verificando si los 3 elementos son iguales y no vacíos
2. **Columnas**: Para cada columna, compara los elementos de las 3 filas
3. **Diagonal principal**: Verifica posiciones (0,0), (1,1), (2,2)
4. **Diagonal secundaria**: Verifica posiciones (0,2), (1,1), (2,0)

### Gestión de Estado
- El juego mantiene estado inmutable una vez finalizado
- Los turnos alternan automáticamente solo en jugadas válidas
- Las jugadas inválidas no afectan el estado del juego
- El tablero se preserva durante manejo de errores

## Manejo de Errores

El juego maneja robustamente los siguientes errores:
- Posiciones ocupadas
- Coordenadas fuera de rango (0-2)
- Entrada de datos inválida
- Intentos de jugar después de que termine el juego

## Requisitos

- Python 3.6+
- No requiere dependencias externas

---

**Desarrollado por Sebastian Merino**  
*Ingeniería en Informática*