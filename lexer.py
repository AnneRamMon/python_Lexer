# Description: Este script implementa un analizador léxico simple para el lenguaje de programación C.
import re  # Módulo de expresiones regulares
import sys  # Módulo de sistema
from collections import defaultdict  # Módulo de colecciones

# Establecer tipos de tokens
token_exprs = [
    # KEYWORDS
    (
        r"auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|printf",
        "KEYWORD",
    ),
    # IDENTIFIERS
    (r"[a-zA-Z_][a-zA-Z_0-9]*\s*\(.*?\)", "IDENTIFIER"),
    # OPERATORS
    (r"\+|\-|\*|\/|\%|\=\=|\!\=|\>|\>\=|\<|\<\=|\&\&|\|\|", "OPERATOR"),
    # CONSTANTS
    (r"\b[0-9]+\b|\d+", "CONSTANT"),  # Números enteros
    # LITERALS
    # main es un ejemplo de cadena de texto
    (r"\".*?\"", "LITERAL"),
    # PUNCTUATION
    (r"\;|\,|\:|\[|\]|\(|\)|\{|\}", "PUNCTUATION"),
    # SPECIAL CHARACTERS
    # Contemplar que < y > son carcaters especiales deben tener una cadena en medio
    (
        r"\\n|\\t|\\r|\\b|\\a|\\f|\\v|\$|\°|\<.*?\>|#include\s*<[^>]*>",
        "SPECIAL CHARACTERS",
    ),
    # SPACE
    (r"\s+", "SPACE"),
    (r"\n", "NEWLINE"),
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
                    line = line[len(value) :]
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
    # Contar tokens por categoría
    token_count = defaultdict(int)
    # Agrupar tokens por categoría
    token_list_by_category = defaultdict(list)

    # Iterar sobre los tokens para contar y agrupar
    for value, tag in tokens:
        if tag not in ["SPACE", "NEWLINE"]:  # Excluir SPACE y NEWLINE
            token_count[tag] += 1
            token_list_by_category[tag].append(value)

    # Presentación de la tabla con ajuste dinámico de ancho
    max_token_length = 50  # Definir un máximo de longitud de tokens por línea para evitar cortes incómodos

    # Determinar el ancho máximo de la columna de tokens
    print(
        "+--------------------+--------+--------------------------------------------------------------+"
    )
    print(
        "| Category           | Count  | Tokens                                                       |"
    )
    print(
        "+--------------------+--------+--------------------------------------------------------------+"
    )

    # Iterar sobre las categorías de tokens
    for category, count in sorted(token_count.items()):
        tokens_list = ", ".join(
            token_list_by_category[category]
        )  # Unir los tokens con comas
        # Dividir la lista de tokens en líneas si es demasiado larga (ajustado a max_token_length)
        tokens_split = [
            tokens_list[i : i + max_token_length]
            for i in range(0, len(tokens_list), max_token_length)
        ]

        # Imprimir la primera línea con la categoría y el conteo
        print(f"| {category:<18} | {count:<6} | {tokens_split[0]:<60} |")

        # Imprimir las líneas restantes con tokens, si las hay
        for line in tokens_split[1:]:
            print(f"| {'':<18} | {'':<6} | {line:<60} |")

    print(
        "+--------------------+--------+--------------------------------------------------------------+"
    )
    print(f"Total tokens: {len(tokens)}")

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
