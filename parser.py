# parser.py

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1][1]
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.tokens[self.pos][0]}")

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos][0] == 'NEWLINE':
                self.pos += 1  # Skip newlines
                continue
            statements.append(self.statement())
        return statements

    def statement(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == 'ID' and token_value == 'let':
            return self.assignment()
        elif token_type == 'ID' and token_value == 'print':
            return self.print_statement()
        else:
            raise SyntaxError("Unknown statement")

    def assignment(self):
        self.consume('ID')  # consume 'let'
        var_name = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.expression()
        self.consume('END')
        return Assign(var_name, expr)

    def print_statement(self):
        self.consume('ID')  # consume 'print'
        self.consume('LPAREN')
        expr = self.expression()
        self.consume('RPAREN')
        self.consume('END')
        return Print(expr)

    def expression(self):
        left = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP':
            op = self.consume('OP')
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == 'NUMBER':
            return Number(self.consume('NUMBER'))
        elif token_type == 'ID':
            return Variable(self.consume('ID'))
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError("Invalid syntax")
