import re

# Established token types

token_exprs = [
    (r'\d+', 'INTEGER'),
    (r'/\*|\+|\-|>=|<=|>|<|==|!=|\*|\/', 'OPERATOR'),
    (r'=', 'ASSIGN'),
    (r'int|main|float|void|return|if|else|while|for|and|or|break|switch|case', 'KEYWORD'),
    (r'\n', 'NEWLINE'),
    (r'\w+', 'IDENTIFIER'),
    (r';|.|,|{|}|\(|\)', 'PUNCTUATION'),

]


print("Enter the code: ")


code_lines = []
while True:
    line = input()
    if line == "":
        break
    code_lines.append(line)


# This function will take the code lines and return the tokens
def lexer(code_lines):
    tokens = []
    for line in code_lines:
        while line:
            match = None
            for token_expr in token_exprs: 
                pattern, tag = token_expr 
                regex = re.compile(pattern) # Compiles the regular expression
                match = regex.match(line) # Matches the regular expression with the line
                if match:
                    value = match.group(0) # Returns the matched string
                    tokens.append((value, tag)) # Appends the token to the list indicating the value and the tag
                    line = line[len(value):] # Removes the token from the line
                    break
            if not match:
                print(f"Error: {line}")
                break
    return tokens

print("Tokens: ")
print(lexer(code_lines))


