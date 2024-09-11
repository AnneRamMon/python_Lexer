import re
import sys
from collections import defaultdict

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
    (r"\".*?\"", "STRING"),  # Cadenas de texto

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
    tokens = []
    for line in code_lines:
        while line:
            match = None
            for regex, tag in token_exprs:
                match = regex.match(line)
                if match:
                    value = match.group(0)
                    if tag != "SPACE":  # Ignorar espacios en blanco
                        tokens.append((value, tag))
                    line = line[len(value):]
                    break
            if not match:
                print(f"Error: Unrecognized token: {line}")
                break
    return tokens

def print_token_summary(tokens):
    # Contar tokens por categoría
    token_count = defaultdict(int)
    token_list_by_category = defaultdict(list)
    
    for value, tag in tokens:
        token_count[tag] += 1
        token_list_by_category[tag].append(value)
    
    # Imprimir el resumen en formato tabular
    print(f"{'Category':<12} {'Count':<6} {'Tokens'}")
    print("="*50)
    for category, count in sorted(token_count.items()):
        tokens_list = ' '.join(token_list_by_category[category])
        if tokens_list.strip():  # Solo imprimir si hay tokens no vacíos
            print(f"{category:<12} {count:<6} {tokens_list}")
        else:
            print(f"{category:<12} {count:<6}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.c>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            code_lines = file.readlines()
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        sys.exit(1)

    tokens = lexer(code_lines)
    print_token_summary(tokens)

if __name__ == "__main__":
    main()