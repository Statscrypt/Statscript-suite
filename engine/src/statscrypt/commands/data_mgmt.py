from typing import List

import statscrypt.core.exceptions as exceptions
from statscrypt.core.expression import ExpressionEvaluator
from statscrypt.core.session import StatSession


def run_use(session: StatSession, variables: List[str]):
    """Implementation of the 'use' command to load a dataset."""
    if not variables:
        raise exceptions.FileError("Please specify a file path.")
    filepath = variables[0].strip('"')

    try:
        session.load_data(filepath)
        return f"Loaded data from {filepath}"
    except FileNotFoundError:
        raise exceptions.FileError(f"File not found at {filepath}")
    except Exception as e:
        raise exceptions.FileError(f"An error occurred: {e}")


def run_gen(session: StatSession, gen_expression: dict, condition: str = None):
    """
    Implementation of the 'gen' command.
    Creates a new variable (column) in the DataFrame based on an expression.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    new_var = gen_expression["new_var"]
    expression = gen_expression["expression"]

    if new_var in session.df.columns:
        raise exceptions.VariableError(f"Variable '{new_var}' already exists.")

    # Evaluate expression
    evaluator = ExpressionEvaluator(session.df)
    try:
        result = evaluator.evaluate(expression)

        # Apply condition if specified
        if condition:
            condition_statement = condition.replace("=", "==")
            mask = session.df.eval(condition_statement)
            session.df[new_var] = None
            session.df.loc[mask, new_var] = result[mask]
        else:
            session.df[new_var] = result

        session.variables = session.df.columns.tolist()
        return f"Variable '{new_var}' generated."
    except Exception as e:
        raise exceptions.SyntaxError(f"Error generating variable: {str(e)}")


def run_list(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'list' command.
    Lists the first 20 rows of the data, optionally filtered.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    target_df = session.df
    if condition:
        condition_statement = condition.replace("=", "==")
        try:
            target_df = session.df.query(condition_statement)
        except Exception as e:
            raise exceptions.SyntaxError(
                f"Error in 'if' condition: {condition_statement} - {e}"
            )

    if not variables:
        return target_df.head(20).to_string(index=False)

    valid_vars = [v for v in variables if v in target_df.columns]
    if not valid_vars:
        raise exceptions.VariableError(f"Variables {variables} not found.")

    return target_df[valid_vars].head(20).to_string(index=False)
