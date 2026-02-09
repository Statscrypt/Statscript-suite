import matplotlib.pyplot as plt
import io
import base64
from statscrypt.core.session import StatSession
from statscrypt.core import exceptions
from typing import List

def run_graph(session: StatSession, variables: List[str]):
    """
    Implementation of the 'graph' command.
    Generates a scatter plot of two variables and returns it as a base64 encoded PNG.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded. Use 'use <file.csv>' first.")

    if len(variables) != 2:
        raise exceptions.SyntaxError("Graph command requires exactly two variables: graph var1 var2")

    var1, var2 = variables[0], variables[1]

    if var1 not in session.df.columns or var2 not in session.df.columns:
        raise exceptions.VariableError(f"Variables '{var1}' or '{var2}' not found in the dataset.")
    
    if not pd.api.types.is_numeric_dtype(session.df[var1]):
        raise exceptions.DataError(f"Variable '{var1}' is not numeric and cannot be plotted.")
    if not pd.api.types.is_numeric_dtype(session.df[var2]):
        raise exceptions.DataError(f"Variable '{var2}' is not numeric and cannot be plotted.")

    plt.figure(figsize=(8, 6))
    plt.scatter(session.df[var1], session.df[var2])
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(f'Scatter plot of {var1} vs {var2}')
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64
