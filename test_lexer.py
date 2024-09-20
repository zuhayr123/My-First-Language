# Import the lexer from the lexer.py file (assuming it's saved as lexer.py)
from lexer import lexer

# The input code to be tokenized
code = """
let x = 10;
let y = 30;
let z = x + y;
print(z);
"""

# Tokenize the code using the lexer
tokens = lexer(code)

# Print the list of tokens
for token in tokens:
    print(token)
