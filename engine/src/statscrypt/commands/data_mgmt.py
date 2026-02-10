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


def run_drop(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'drop' command.
    Drops variables or observations based on condition.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if condition:
        # Drop observations matching condition
        try:
            mask = session.df.eval(condition)
            initial_count = len(session.df)
            session.df = session.df[~mask]
            dropped_count = initial_count - len(session.df)
            return f"Dropped {dropped_count} observations."
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")
    elif variables:
        # Drop variables
        missing_vars = [v for v in variables if v not in session.df.columns]
        if missing_vars:
            raise exceptions.VariableError(f"Variables not found: {missing_vars}")

        session.df = session.df.drop(columns=variables)
        session.variables = session.df.columns.tolist()
        return f"Dropped variables: {', '.join(variables)}"
    else:
        raise exceptions.SyntaxError(
            "drop requires either variables or an 'if' condition"
        )


def run_keep(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'keep' command.
    Keeps only specified variables or observations matching condition.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if condition:
        # Keep observations matching condition
        try:
            mask = session.df.eval(condition)
            initial_count = len(session.df)
            session.df = session.df[mask]
            kept_count = len(session.df)
            return f"Kept {kept_count} of {initial_count} observations."
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")
    elif variables:
        # Keep variables
        missing_vars = [v for v in variables if v not in session.df.columns]
        if missing_vars:
            raise exceptions.VariableError(f"Variables not found: {missing_vars}")

        session.df = session.df[variables]
        session.variables = session.df.columns.tolist()
        return f"Kept variables: {', '.join(variables)}"
    else:
        raise exceptions.SyntaxError(
            "keep requires either variables or an 'if' condition"
        )


def run_save(session: StatSession, variables: List[str]):
    """
    Implementation of the 'save' command.
    Saves the current dataset to a CSV file.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if not variables:
        raise exceptions.SyntaxError("save requires a filename")

    filepath = variables[0].strip('"')

    try:
        session.df.to_csv(filepath, index=False)
        return f"Data saved to {filepath}"
    except Exception as e:
        raise exceptions.FileError(f"Error saving file: {str(e)}")


def run_count(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'count' command.
    Counts observations, optionally with a condition.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if condition:
        try:
            mask = session.df.eval(condition)
            count = mask.sum()
            return f"{count}"
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")
    else:
        return f"{len(session.df)}"
