import re # Regular Expressions
import sys # System-specific parameters and functions
from collections import defaultdict # Container datatypes
import tkinter as tk # Standard Python interface to the Tk GUI toolkit
from tkinter import ttk # Themed Tkinter
from PIL import ImageGrab # Python Imaging Library

# Define the regular expressions for each token type
    #NOTE: Consider the order of the regular expressions, as the first match will be used
#(r"pattern", "tag")
    # tag: Token type
    # pattern: Regular expression pattern
token_exprs = [
    #KEYWORDS
    (r"auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|printf|include", "KEYWORD"),
    #IDENTIFIER
    (r"[a-zA-Z_$][a-zA-Z_$0-9]*", "IDENTIFIER"),
    #OTHERS
    (r"\s*<[^>]*>|\<.*?\>", "OTHER"),
    #OPERATORS
    (r"\+|\-|\*|\/|\%|\=\=|\!\=|\>|\>\=|\<|\<\=|\&\&|\|\||\=|\<\<|\>\>|\<\<\=|\>\>\=|\?|\:", "OPERATOR"),
    #COMMENT
    (r"\/\/.*", "COMMENT"),
    #CONSTANT
    (r"\b[0-9]+\b|\d+", "CONSTANT"),
    #LITERAL
    (r"\".*?\"|\'.\'", "LITERAL"),
    #PUNCTUATION
    (r"\;|\,|\:|\[|\]|\(|\)|\{|\}", "PUNCTUATION"),
    #SPECIAL CHARACTERS
    (r"\°|\#|\&", "SPECIAL CHARACTERS"),
    #SPACE
    (r"\s+", "SPACE"),
    #NEWLINE
    (r"\n", "NEWLINE"),
]

# Compile the regular expressions
token_exprs = [(re.compile(pattern), tag) for pattern, tag in token_exprs]

# Function to generate tokens from the code lines
def lexer(code_lines):
    # List to store the generated tokens
    tokens = []
    # Set to track unique tokens
    seen_tokens = set()  # Set to track unique tokens
    total_token_count = 0  # Counter for all valid tokens generated

    # Define the token types to exclude from counting and adding
    excluded_tags = {"COMMENT", "NEWLINE", "SPACE", "OTHER"}

    # Iterate over the code lines
    for line in code_lines:
        # Iterate over the line to generate tokens
        while line:
            # Flag to check if a match is found
            match = None
            # Iterate over the token expressions
            for regex, tag in token_exprs:
                # Match the regular expression with the line
                match = regex.match(line)
                # If a match is found, create a token and update the line
                if match:
                    # Get the matched value
                    value = match.group(0)
                    # Create the token
                    token = (value, tag)

                    # Only increment token count and track tokens if not excluded
                    if tag not in excluded_tags:
                        total_token_count += 1  # Count every valid token
                        # Add to seen tokens only if not already seen
                        if token not in seen_tokens:
                            seen_tokens.add(token) # Add to seen tokens
                    
                    line = line[len(value):]  # Move to the next part of the line
                    break # Break the loop to start matching from the beginning of the line
            # If no match is found, print an error and break the loop
            if not match:
                # Print an error message
                print(f"Error: Unrecognized token: {line}")
                break
    # Return the total token count and the seen tokens
    return total_token_count, seen_tokens

# Function to display the token summary
def show_token_summary(num_tokens, tokens):
    # Dictionary to store the token count for each category
    token_count = defaultdict(int)
    # Dictionary to store the tokens for each category
    token_list_by_category = defaultdict(list)
    # Total tokens
    total_tokens = num_tokens

    # Iterate over the tokens
    for value, tag in tokens:
        # Increment the token count for the category
        if tag not in ["SPACE", "NEWLINE", "COMMENT", "OTHER"]: # Exclude these tags
            token_count[tag] += 1 # Increment the token count
            token_list_by_category[tag].append(value) # Add the token to the list

    root = tk.Tk() # Create the main window
    root.title("Token's Summary") # Set the title

    # Set the style for the treeview
    style = ttk.Style()
    # Set the style for the heading
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="gray25", foreground="black")
    # Set the style for the treeview
    style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")

    # Create the title label
    title = tk.Label(root, text="Token's Summary", font=("Helvetica", 16, "bold"), fg="gray25")
    # Pack the title label
    title.pack(pady=10)

    # Create the treeview
    tree = ttk.Treeview(root, columns=("Category", "Count", "Tokens"), show="headings")
    # Set the headings
    tree.heading("Category", text="Category")
    # Set the headings
    tree.heading("Count", text="Count")
    # Set the headings
    tree.heading("Tokens", text="Tokens")

    # Set the tags for the treeview rows
    tree.tag_configure("oddrow", background="gray85")
    # Set the tags for the treeview rows
    tree.tag_configure("evenrow", background="gray95")

    # Insert the data into the treeview
    for idx, (category, count) in enumerate(sorted(token_count.items())):
        # Get the tokens for the category
        tokens_str = ", ".join(token_list_by_category[category])
        # Set the tag for the row
        tag = "oddrow" if idx % 2 == 0 else "evenrow"
        # Insert the row into the treeview
        tree.insert("", "end", values=(category, count, tokens_str), tags=(tag,))

    # Pack the treeview
    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Set the column width
    tree.column("Category", width=100, minwidth=80)
    tree.column("Count", width=80, minwidth=60)
    tree.column("Tokens", width=300, minwidth=200)

    # Create the save button
    save_button = tk.Button(root, text="Save as Image", command=lambda: save_window_as_image(root))
    save_button.pack(pady=10)

    # Create the total label
    total_label = tk.Label(root, text=f"Total tokens: {total_tokens}", font=("Helvetica", 14, "bold"), fg="red")
    total_label.pack(pady=10)

    # Run the main loop
    root.mainloop()

# Function to save the window as an image
def save_window_as_image(window, filename="screenshot.png"):
    # Get the window dimensions
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()

    # Take a screenshot of the window
    ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(filename)
    print(f"Screenshot saved as {filename}")

# Main function
def main():
    # Check if the filename is provided
    if len(sys.argv) != 2:
        # Print the usage
        print(f"Usage: {sys.argv[0]} <file.c>")
        # Exit the program
        sys.exit(1)
    
    # Get the filename
    filename = sys.argv[1]
    # Read the code lines from the file
    try:
        # Open the file
        with open(filename, "r") as file:
            # Read the code lines
            code_lines = file.readlines()
    # Handle the file reading error
    except IOError as e:
        # Print the error message
        print(f"Error reading file {filename}: {e}")
        # Exit the program
        sys.exit(1)

    # Generate the tokens
    num_tokens, tokens = lexer(code_lines)
    # Display the token summary
    show_token_summary(num_tokens, tokens)

# Entry point of the program
if __name__ == "__main__":
    # Call the main function
    main()