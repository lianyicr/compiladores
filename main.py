# -*- coding: utf-8 -*-
import sys
from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer, SemanticError

def main():
    # Por defecto carga el archivo de prueba semánticamente incorrecto para ver el error
    # Puedes pasarlo por argumento desde la consola: python main.py examples/prueba_valida.set
    filepath = "examples/prueba_error_semantico.set"
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filepath}'")
        return

    # IMPORTANTE: Alimentar el lexer antes del parseo para que los cálculos 
    # de columnas en ast_nodes encuentren los saltos de línea correctamente.
    lexer.input(source)

    # FASE 2: Análisis Sintáctico (genera el AST)
    ast = parser.parse(source, lexer=lexer)

    if ast is None:
        print("El análisis sintáctico falló. No se pudo generar el AST.")
        return

    # FASE 3: Análisis Semántico
    checker = SemanticAnalyzer()
    
    try:
        checker.visit(ast)
        print("Programa semánticamente correcto.")
    except SemanticError as e:
        # Aquí atrapamos nuestra excepción personalizada e imprimimos el error limpio
        print(e)
    except Exception as e:
        # Fallback para cualquier otro error imprevisto
        print(f"Error interno del compilador: {e}")

if __name__ == "__main__":
    main()
