import re
import sys

# Establecer tipos de tokens
token_exprs = [
    (r"\<.*\>", "LIBRARY"),
    (r"\d+", "INTEGER"),
    (r"\+\+|--|\+|-|\*|/|>=|<=|>|<|==|!=|=|&&|\|\||%|\||\(", "OPERATOR"),
    (
        r"\bint\b|\binclude\b|\bprintf\b|\bmain\b|\bfloat\b|\bvoid\b|\breturn\b|\bif\b|\belse\b|\bwhile\b|\bfor\b|\bbreak\b|\bswitch\b|\bcase\b",
        "KEYWORD",
    ),
    (r"\n", "NEWLINE"),
    (r"[a-zA-Z_][a-zA-Z_0-9]*", "IDENTIFIER"),
    (r"\".*?\"", "STRING"),
    (r"\s+", "SPACE"),
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
                    if tag != "SPACE":
                        tokens.append((value, tag))
                    line = line[len(value) :]
                    break
            if not match:
                print(f"Error: Unrecognized token: {line}")
                break
    return tokens


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
    print("Tokens:")
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
