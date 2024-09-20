#!/usr/bin/env python3
import sys
from lexer import lexer
from parser import Parser, Number, BinOp, Variable, Assign, Print
from ast_visualizer import ASTVisualizer

class Interpreter:
    def __init__(self):
        self.variables = {}

    def eval(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, BinOp):
            left_val = self.eval(node.left)
            right_val = self.eval(node.right)
            if node.op == '+':
                return left_val + right_val
            elif node.op == '-':
                return left_val - right_val
            elif node.op == '*':
                return left_val * right_val
            elif node.op == '/':
                return left_val / right_val
        elif isinstance(node, Variable):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise NameError(f"Variable '{node.name}' is not defined")
        elif isinstance(node, Assign):
            value = self.eval(node.value)
            self.variables[node.name] = value
        elif isinstance(node, Print):
            value = self.eval(node.expression)
            print(value)
        else:
            raise TypeError("Unknown node type")

def main():
    # Check if the file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <source_file>")
        sys.exit(1)

    # Get the file path from command-line arguments
    source_file = sys.argv[1]

    # Read the source code from the file
    with open(source_file, 'r') as file:
        source_code = file.read()

    # Lexical analysis
    tokens = lexer(source_code)
    print("Tokens:", tokens)

    # Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    visualizer = ASTVisualizer()
    for stmt in ast:
        visualizer.visualize(stmt)

    visualizer.render('ast')
    print("AST:", ast)

    # Interpreting
    interpreter = Interpreter()
    for stmt in ast:
        interpreter.eval(stmt)

if __name__ == "__main__":
    main()
