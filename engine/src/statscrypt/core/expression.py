import ast
import operator

import numpy as np
import pandas as pd
import statscrypt.core.exceptions as exceptions

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

FUNCTIONS = {
    "log": np.log,
    "exp": np.exp,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "ln": np.log,
}


class ExpressionEvaluator:
    """Evaluates mathematical expressions for gen command."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def evaluate(self, expression: str) -> pd.Series:
        """Evaluate expression and return pandas Series."""
        try:
            tree = ast.parse(expression, mode="eval")
            return self._eval_node(tree.body)
        except Exception as e:
            raise exceptions.SyntaxError(f"Invalid expression '{expression}': {str(e)}")

    def _eval_node(self, node):
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.Name):
            # Variable reference
            if node.id in self.df.columns:
                return self.df[node.id]
            else:
                raise exceptions.VariableError(
                    f"Variable '{node.id}' not found in dataset"
                )
        elif isinstance(node, ast.BinOp):
            # Binary operation (+, -, *, /, **)
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = OPERATORS.get(type(node.op))
            if op:
                return op(left, right)
            else:
                raise exceptions.SyntaxError(f"Unsupported operator: {type(node.op)}")
        elif isinstance(node, ast.UnaryOp):
            # Unary operation (-, +)
            operand = self._eval_node(node.operand)
            op = OPERATORS.get(type(node.op))
            if op:
                return op(operand)
            else:
                raise exceptions.SyntaxError(
                    f"Unsupported unary operator: {type(node.op)}"
                )
        elif isinstance(node, ast.Call):
            # Function call
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in FUNCTIONS:
                    if len(node.args) != 1:
                        raise exceptions.SyntaxError(
                            f"Function '{func_name}' expects 1 argument"
                        )
                    arg = self._eval_node(node.args[0])
                    return FUNCTIONS[func_name](arg)
                else:
                    raise exceptions.SyntaxError(f"Unknown function: {func_name}")
            else:
                raise exceptions.SyntaxError("Invalid function call")
        else:
            raise exceptions.SyntaxError(f"Unsupported expression type: {type(node)}")
