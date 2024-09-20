from graphviz import Digraph
from parser import Parser, Number, BinOp, Variable, Assign, Print

class ASTVisualizer:
    def __init__(self):
        self.graph = Digraph(format='png')
        self.node_count = 0

    def add_node(self, label):
        node_id = str(self.node_count)
        self.graph.node(node_id, label)
        self.node_count += 1
        return node_id

    def visualize(self, node):
        if isinstance(node, Number):
            return self.add_node(f"Number({node.value})")
        elif isinstance(node, BinOp):
            op_node = self.add_node(f"Op({node.op})")
            left_node = self.visualize(node.left)
            right_node = self.visualize(node.right)
            self.graph.edge(op_node, left_node)
            self.graph.edge(op_node, right_node)
            return op_node
        elif isinstance(node, Variable):
            return self.add_node(f"Variable({node.name})")
        elif isinstance(node, Assign):
            assign_node = self.add_node("Assign")
            var_node = self.add_node(f"Variable({node.name})")
            value_node = self.visualize(node.value)
            self.graph.edge(assign_node, var_node)
            self.graph.edge(assign_node, value_node)
            return assign_node
        elif isinstance(node, Print):
            print_node = self.add_node("Print")
            expr_node = self.visualize(node.expression)
            self.graph.edge(print_node, expr_node)
            return print_node

    def render(self, filename='ast'):
        self.graph.render(filename, view=True)
