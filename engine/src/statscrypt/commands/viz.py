import base64
import io
from typing import List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from statscrypt.core import exceptions
from statscrypt.core.session import StatSession


def run_graph(session: StatSession, variables: List[str]):
    """
    Implementation of the 'graph' command.
    - Single variable: creates a histogram
    - Two variables: creates a scatter plot
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded. Use 'use <file.csv>' first.")

    if len(variables) == 0 or len(variables) > 2:
        raise exceptions.SyntaxError(
            "Graph command requires 1 or 2 variables: graph var1 [var2]"
        )

    # Single variable: histogram
    if len(variables) == 1:
        var1 = variables[0]
        if var1 not in session.df.columns:
            raise exceptions.VariableError(
                f"Variable '{var1}' not found in the dataset."
            )
        if not pd.api.types.is_numeric_dtype(session.df[var1]):
            raise exceptions.DataError(
                f"Variable '{var1}' is not numeric and cannot be plotted."
            )

        plt.figure(figsize=(8, 6))
        plt.hist(session.df[var1], bins=20, edgecolor="black", alpha=0.7)
        plt.xlabel(var1)
        plt.ylabel("Frequency")
        plt.title(f"Histogram of {var1}")
        plt.grid(True, alpha=0.3)

    # Two variables: scatter plot
    else:
        var1, var2 = variables[0], variables[1]

        if var1 not in session.df.columns or var2 not in session.df.columns:
            raise exceptions.VariableError(
                f"Variables '{var1}' or '{var2}' not found in the dataset."
            )

        if not pd.api.types.is_numeric_dtype(session.df[var1]):
            raise exceptions.DataError(
                f"Variable '{var1}' is not numeric and cannot be plotted."
            )
        if not pd.api.types.is_numeric_dtype(session.df[var2]):
            raise exceptions.DataError(
                f"Variable '{var2}' is not numeric and cannot be plotted."
            )

        plt.figure(figsize=(8, 6))
        plt.scatter(session.df[var1], session.df[var2], alpha=0.6)
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.title(f"Scatter plot: {var1} vs {var2}")
        plt.grid(True, alpha=0.3)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return image_base64
