# Description: Este script implementa un analizador léxico simple para el lenguaje de programación C.
import re # Módulo de expresiones regulares
import sys # Módulo de sistema
from collections import defaultdict # Módulo de colecciones

# Establecer tipos de tokens
token_exprs = [
    # Comentarios (deben ir primero para evitar que se confundan con otros patrones)
    (r"//.*", "COMMENT"),  # Comentarios de una sola línea
    (r"/\*.*?\*/", "COMMENT"),  # Comentarios multilínea

    # Directivas del preprocesador (también deben ir antes para evitar confusión)
    (r"#include\s*<[^>]+>", "DIRECTIVE"),  # Directivas de inclusión como #include <stdio.h>
    (r"#define\s+\w+\s+[^#\n]+", "DIRECTIVE"),  # Definiciones de macros como #define MAX 100
    
    # Palabras clave
    (r"\bint\b|\binclude\b|\bprintf\b|\bmain\b|\bfloat\b|\bvoid\b|\breturn\b|\bif\b|\belse\b|\bwhile\b|\bfor\b|\bbreak\b|\bswitch\b|\bcase\b|\bchar\b|\bdouble\b|\blong\b|\bshort\b|\bsigned\b|\bunsigned\b", "KEYWORD"),
    
    # Identificadores
    (r"[a-zA-Z_][a-zA-Z_0-9]*", "IDENTIFIER"),
    
    # Operadores (deben ir antes de los literales para evitar confusión)
    (r"\+\+|--|\+|-|\*|/|>=|<=|>|<|==|!=|=|&&|\|\||%|\||\&|\^|\~|\(|\)|\[\]|\{\}|->|\.", "OPERATOR"),
    
    # Literales (números y cadenas)
    (r"\d+", "CONSTANT"),  # Números enteros
    (r"\".*?\"", "LITERAL"),  # Cadenas de texto

    # Librerías (deben ir después de los identificadores y palabras clave)
    (r"<[^>]+>", "LIBRARY"),  # Librerías entre corchetes angulares
    
    # Delimitadores y puntuación (deben ir al final para no interferir con otros patrones)
    (r"\n", "NEWLINE"),  # Nueva línea
    (r"\s+", "SPACE"),  # Espacios en blanco
    (r";|\.|,|{|}|\(|\)", "PUNCTUATION"),
]

# Compilar expresiones regulares una vez
token_exprs = [(re.compile(pattern), tag) for pattern, tag in token_exprs]

# Función para analizar cadenas de código
def lexer(code_lines):
    # Lista de tokens
    tokens = []
    # Analizar cada línea de código
    for line in code_lines:
        # Iterar sobre la línea de código hasta que se consuma completamente
        while line:
            # Buscar el siguiente token en la línea
            match = None
            # Iterar sobre los patrones de expresión regular
            for regex, tag in token_exprs:
                # Intentar hacer coincidir el patrón con el inicio de la línea
                match = regex.match(line)
                # Si hay coincidencia
                if match:
                    # Obtener el valor del token y agregarlo a la lista
                    value = match.group(0)
                    # Ignorar espacios en blanco y nuevas líneas
                    if tag != "SPACE":  # Ignorar espacios en blanco
                        # Agregar el token a la lista
                        tokens.append((value, tag))
                    # Actualizar la línea para continuar con el siguiente token
                    line = line[len(value):]
                    break
            # Si no se encontró ninguna coincidencia, imprimir un mensaje de error
            if not match:
                # Imprimir mensaje de error
                print(f"Error: Unrecognized token: {line}")
                break
    # Devolver la lista de tokens
    return tokens

# Función para imprimir un resumen de los tokens
def print_token_summary(tokens):
#Nota : defaultdict es una subclase de dict que permite definir un valor predeterminado para las claves que no existen.
    # Contar tokens por categoría
    token_count = defaultdict(int)
    # Agrupar tokens por categoría
    token_list_by_category = defaultdict(list)
    # Iterar sobre los tokens
    for value, tag in tokens:
        # Contar el token
        token_count[tag] += 1
        # Agregar el token a la lista de tokens por categoría
        token_list_by_category[tag].append(value)
    
    # Imprimir el resumen en formato tabular
    print(f"{'Category':<12} {'Count':<6} {'Tokens'}")
    # Imprimir separador
    print("="*50)
    # Iterar sobre las categorías de tokens
    for category, count in sorted(token_count.items()):
        # Imprimir el nombre de la categoría, el recuento y los
        tokens_list = ' '.join(token_list_by_category[category])
        if tokens_list.strip():  # Solo imprimir si hay tokens no vacíos
            print(f"{category:<12} {count:<6} {tokens_list}")
        else:
            print(f"{category:<12} {count:<6}") # Imprimir solo el nombre de la categoría y el recuento

# Función principal
def main():
    # Verificar argumentos de línea de comandos
    if len(sys.argv) != 2:
        # Imprimir mensaje de uso
        print(f"Usage: {sys.argv[0]} <file.c>")
        # Salir con código de error
        sys.exit(1)

    # Obtener el nombre del archivo de código fuente
    filename = sys.argv[1]

    # Leer el archivo de código fuente
    try:
        # Leer todas las líneas del archivo
        with open(filename, "r") as file:
            code_lines = file.readlines()
    # Manejar errores de lectura
    except IOError as e:
        # Imprimir mensaje de error
        print(f"Error reading file {filename}: {e}")
        # Salir con código de error
        sys.exit(1)

    # Analizar el código fuente
    tokens = lexer(code_lines)
    # Imprimir resumen de tokens
    print_token_summary(tokens)

# Ejecutar el programa principal
if __name__ == "__main__":
    # Llamar a la función principal
    main()