import re
import sys
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab

# Establecer tipos de tokens
token_exprs = [
    (r"auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|printf|include", "KEYWORD"),
    (r"[a-zA-Z_][a-zA-Z_0-9]*", "IDENTIFIER"),
    (r"\s*<[^>]*>|\<.*?\>", "OTHER"),
    (r"\+|\-|\*|\/|\%|\=\=|\!\=|\>|\>\=|\<|\<\=|\&\&|\|\||\=|\<\<|\>\>|\<\<\=|\>\>\=", "OPERATOR"),
    #COMMENT
    (r"\/\/.*", "COMMENT"),
    (r"\b[0-9]+\b|\d+", "CONSTANT"),
    (r"\".*?\"", "LITERAL"),
    (r"\;|\,|\:|\[|\]|\(|\)|\{|\}", "PUNCTUATION"),
    (r"\\n|\\t|\\r|\\b|\\a|\\f|\\v|\$|\°|\#|\&", "SPECIAL CHARACTERS"),
    (r"\s+", "SPACE"),
    (r"\n", "NEWLINE"),
]

# Convertir los patrones en expresiones regulares
token_exprs = [(re.compile(pattern), tag) for pattern, tag in token_exprs]

def lexer(code_lines):
    tokens = []
    seen_tokens = set()  # Set to track unique tokens
    total_token_count = 0  # Counter for all valid tokens generated

    # Define the token types to exclude from counting and adding
    excluded_tags = {"COMMENT", "NEWLINE", "SPACE", "OTHER"}

    for line in code_lines:
        while line:
            match = None
            for regex, tag in token_exprs:
                match = regex.match(line)
                if match:
                    value = match.group(0)
                    token = (value, tag)

                    # Only increment token count and track tokens if not excluded
                    if tag not in excluded_tags:
                        total_token_count += 1  # Count every valid token
                        # Add to seen tokens only if not already seen
                        if token not in seen_tokens:
                            seen_tokens.add(token)
                    
                    line = line[len(value):]  # Move to the next part of the line
                    break
            if not match:
                print(f"Error: Unrecognized token: {line}")
                break

    return total_token_count, seen_tokens

def show_token_summary(num_tokens, tokens):
    token_count = defaultdict(int)
    token_list_by_category = defaultdict(list)
    total_tokens = num_tokens

    for value, tag in tokens:
        if tag not in ["SPACE", "NEWLINE", "COMMENT", "OTHER"]:
            token_count[tag] += 1
            token_list_by_category[tag].append(value)

    root = tk.Tk()
    root.title("Token's Summary")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="gray25", foreground="black")
    style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")

    title = tk.Label(root, text="Token's Summary", font=("Helvetica", 16, "bold"), fg="gray25")
    title.pack(pady=10)

    tree = ttk.Treeview(root, columns=("Category", "Count", "Tokens"), show="headings")
    tree.heading("Category", text="Category")
    tree.heading("Count", text="Count")
    tree.heading("Tokens", text="Tokens")

    tree.tag_configure("oddrow", background="gray85")
    tree.tag_configure("evenrow", background="gray95")

    for idx, (category, count) in enumerate(sorted(token_count.items())):
        tokens_str = ", ".join(token_list_by_category[category])
        tag = "oddrow" if idx % 2 == 0 else "evenrow"
        tree.insert("", "end", values=(category, count, tokens_str), tags=(tag,))

    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Ajustar ancho de columnas
    tree.column("Category", width=100, minwidth=80)
    tree.column("Count", width=80, minwidth=60)
    tree.column("Tokens", width=300, minwidth=200)

    save_button = tk.Button(root, text="Save as Image", command=lambda: save_window_as_image(root))
    save_button.pack(pady=10)

    total_label = tk.Label(root, text=f"Total tokens: {total_tokens}", font=("Helvetica", 14, "bold"), fg="red")
    total_label.pack(pady=10)

    root.mainloop()

def save_window_as_image(window, filename="screenshot.png"):
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()

    ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(filename)
    print(f"Screenshot saved as {filename}")

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

    num_tokens, tokens = lexer(code_lines)
    show_token_summary(num_tokens, tokens)

if __name__ == "__main__":
    main()