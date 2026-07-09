# Compilador SetLang

Proyecto de implementación de un Lenguaje de Dominio Específico (DSL) para la manipulación y evaluación de conjuntos finitos. El compilador abarca las tres fases fundamentales del análisis de lenguajes: análisis léxico, análisis sintáctico y análisis semántico.

## Descripción del DSL
SetLang es un lenguaje diseñado para la manipulación, evaluación y exploración de conjuntos finitos. Provee una sintaxis clara y matemáticamente intuitiva para realizar operaciones como unión, intersección, diferencia y comprobación de pertenencia.

## Características
* Análisis Léxico: Reconocimiento de palabras reservadas, identificadores, literales y operadores mediante expresiones regulares.
* Análisis Sintáctico: Construcción de un Árbol de Sintaxis Abstracta (AST) utilizando PLY (Python Lex-Yacc).
* Análisis Semántico: Validación de tipos, reglas de homogeneidad de conjuntos, verificación de ámbitos (scopes) y chequeo de declaraciones previas.
* Reporte de Errores: Mensajes detallados que incluyen la línea y columna exacta del error.
* Recuperación de Errores: Implementación de "Modo Pánico" para el manejo de errores sintácticos, permitiendo continuar el análisis.

## Requisitos
* Python 3.8 o superior.
* PLY (Python Lex-Yacc): Librería requerida para el procesamiento de la gramática.

Para instalar la dependencia, ejecute:
```
pip install ply
```
Para analizar un archivo de código fuente escrito en SetLang, ejecuta el archivo principal pasándole la ruta del programa como argumento desde la línea de comandos:
```
python main.py prueba_valida.set 
```
Si el programa no contiene errores léxicos, sintácticos ni semánticos, la consola mostrará el mensaje:
```
Programa semánticamente correcto.
```
En caso de encontrar una violación a las reglas, el compilador abortará su ejecución imprimiendo con exactitud el tipo de error, la línea, la columna y la regla que fue violada.
