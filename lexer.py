import re

# Updated token types to include parentheses
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
    ('ASSIGN',   r'='),             # Assignment operator
    ('END',      r';'),             # Statement terminator
    ('ID',       r'[A-Za-z]+'),     # Identifiers
    ('PRINT',    r'print'),         # Print statement
    ('LET',      r'let'),           # Variable declaration
    ('OP',       r'[+\-*/]'),       # Arithmetic operators
    ('LPAREN',   r'\('),            # Left parenthesis
    ('RPAREN',   r'\)'),            # Right parenthesis
    ('NEWLINE',  r'\n'),            # Line endings
    ('SKIP',     r'[ \t]+'),        # Skip spaces and tabs
    ('MISMATCH', r'.'),             # Any other character
]

def lexer(code):
    tokens = []
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
    get_token = re.compile(token_regex).match
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if match:
            kind = match.lastgroup
            value = match.group(kind)
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'SKIP':
                pos = match.end()
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character {value!r}')
            tokens.append((kind, value))
            pos = match.end()
        else:
            raise RuntimeError(f'Unexpected character {code[pos]!r}')
    return tokens
