# Description: Program to analyze C code and show a summary of tokens using Tkinter
import re  # Módulo para expresiones regulares
import sys  # Módulo para interactuar con el sistema operativo
from collections import defaultdict  # Diccionario con valores por defecto
import tkinter as tk  # Módulo para crear interfaces gráficas
from tkinter import ttk  # Módulo para crear tablas
from PIL import ImageGrab  # Módulo para capturar imágenes de la pantalla

# Establecer tipos de tokens
token_exprs = [
    # KEYWORDS
    (
        r"auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|printf|include",
        "KEYWORD",
    ),
    # IDENTIFIERS
    (r"[a-zA-Z_][a-zA-Z_0-9]*", "IDENTIFIER"),
    # OPERATORS
    (r"\+|\-|\*|\/|\%|\=\=|\!\=|\>|\>\=|\<|\<\=|\&\&|\|\|", "OPERATOR"),
    # CONSTANTS
    (r"\b[0-9]+\b|\d+", "CONSTANT"),
    # LITERALS
    (r"\".*?\"", "LITERAL"),
    # PUNCTUATION
    (r"\;|\,|\:|\[|\]|\(|\)|\{|\}", "PUNCTUATION"),
    # SPECIAL CHARACTERS
    (r"\\n|\\t|\\r|\\b|\\a|\\f|\\v|\$|\°|\<.*?\>|\#|\s*<[^>]*>", "SPECIAL CHARACTERS"),
    # SPACE
    (r"\s+", "SPACE"),
    # NEWLINE
    (r"\n", "NEWLINE"),
]

# Convertir los patrones en expresiones regulares
token_exprs = [(re.compile(pattern), tag) for pattern, tag in token_exprs]


# Función para analizar cadenas de código
def lexer(code_lines):
    # Lista de tokens
    tokens = []
    # Recorrer cada línea de código
    for line in code_lines:
        # Recorrer cada token en la línea
        while line:
            # Inicializar variable de coincidencia
            match = None
            # Recorrer cada expresión regular
            for regex, tag in token_exprs:
                # Buscar coincidencia en la línea
                match = regex.match(line)
                # Si hay coincidencia
                if match:
                    # Obtener valor del token
                    value = match.group(0)
                    # Agregar token a la lista
                    if tag != "SPACE":
                        # Agregar token a la lista
                        tokens.append((value, tag))
                    # Actualizar línea
                    line = line[len(value) :]
                    # Salir del bucle
                    break
            # Si no hay coincidencia
            if not match:
                # Mostrar error
                print(f"Error: Unrecognized token: {line}")
                # Salir del bucle
                break
    # Retornar lista de tokens
    return tokens


# Función para mostrar una tabla con Tkinter
def show_token_summary(tokens):
    # Contar tokens por categoría
    token_count = defaultdict(int)
    # Lista de tokens por categoría
    token_list_by_category = defaultdict(list)
    # Contar el número total de tokens
    total_tokens = len(tokens)

    # Recorrer cada token
    for value, tag in tokens:
        # Ignorar tokens de espacio y nueva línea
        if tag not in ["SPACE", "NEWLINE"]:
            # Contar tokens por categoria
            token_count[tag] += 1
            # Agregar token a la lista por categoría
            token_list_by_category[tag].append(value)

    # Crear ventana de Tkinter
    root = tk.Tk()
    # Establecer título de la ventana
    root.title("Token's Summary")

    # Crear un estilo personalizado para la tabla
    style = ttk.Style()
    # Establecer colores de fondo y texto
    style.configure(
        "Treeview.Heading",
        font=("Helvetica", 12, "bold"),
        background="gray25",
        foreground="black",
    )
    # Establecer colores de fondo y texto
    style.configure(
        "Treeview", rowheight=25, borderwidth=1, relief="solid"
    )  # Bordes en las celdas

    # Crear el título superior
    title = tk.Label(
        root, text="Token's Summary", font=("Helvetica", 16, "bold"), fg="gray25"
    )
    # Empaquetar el título en la ventana
    title.pack(pady=10)

    # Crear tabla utilizando ttk.Treeview
    tree = ttk.Treeview(root, columns=("Category", "Count", "Tokens"), show="headings")
    # Establecer encabezados de las columnas
    tree.heading("Category", text="Category")
    # Establecer encabezados de las columnas
    tree.heading("Count", text="Count")
    # Establecer encabezados de las columnas
    tree.heading("Tokens", text="Tokens")

    # Colores monocromáticos para las filas
    tree.tag_configure("oddrow", background="gray85")
    # Colores monocromáticos para las filas
    tree.tag_configure("evenrow", background="gray95")

    # Insertar datos en la tabla con colores alternos
    for idx, (category, count) in enumerate(sorted(token_count.items())):
        # Obtener tokens por categoría
        tokens_str = ", ".join(token_list_by_category[category])
        # Establecer color de la fila
        tag = "oddrow" if idx % 2 == 0 else "evenrow"
        # Insertar fila en la tabla
        tree.insert("", "end", values=(category, count, tokens_str), tags=(tag,))

    # Empaquetar tabla en la ventana
    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Ajustar estilo de bordes en las columnas
    for col in tree["columns"]:
        # Ajustar ancho de las columnas
        tree.column(
            col, width=150, minwidth=150, stretch=tk.NO
        )  # Ancho fijo y sin estiramiento

    # Botón para guardar la ventana como imagen
    save_button = tk.Button(
        root, text="Save as Image", command=lambda: save_window_as_image(root)
    )
    save_button.pack(pady=10)
    # Mostrar el número total de tokens en rojo
    total_label = tk.Label(
        root,
        text=f"Total tokens: {total_tokens}",
        font=("Helvetica", 14, "bold"),
        fg="red",
    )
    total_label.pack(pady=10)

    # Ejecutar la ventana
    root.mainloop()

# Función para capturar y guardar la ventana como una imagen
def save_window_as_image(window, filename="screenshot.png"):
    # Obtener las coordenadas de la ventana
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()

    # Capturar la pantalla de la región de la ventana
    ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(filename)
    print(f"Screenshot saved as {filename}")


# Función principal
def main():
    # Verificar argumentos
    if len(sys.argv) != 2:
        # Mostrar mensaje de uso
        print(f"Usage: {sys.argv[0]} <file.c>")
        # Salir del programa
        sys.exit(1)
    # Obtener nombre del archivo
    filename = sys.argv[1]

    # Leer el archivo
    try:
        # Leer todas las líneas del archivo
        with open(filename, "r") as file:
            # Leer todas las líneas del archivo
            code_lines = file.readlines()
    # Manejar error de lectura
    except IOError as e:
        # Mostrar mensaje de error
        print(f"Error reading file {filename}: {e}")
        # Salir del programa
        sys.exit(1)

    # Analizar el código
    tokens = lexer(code_lines)
    # Mostrar resumen de tokens
    show_token_summary(tokens)


# Ejecutar el programa principal
if __name__ == "__main__":
    # Ejecutar el programa principal
    main()
