from typing import List

import pandas as pd
import statscrypt.core.exceptions as exceptions
from statscrypt.core.session import StatSession

try:
    import statsmodels.api as sm

    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False


def run_summarize(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'summarize' command.
    Applies an optional 'if' condition before summarizing.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")
    target_df = session.df
    if condition:
        try:
            target_df = session.df.query(condition)
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")

    if not variables:
        return target_df.describe().to_string()

    valid_vars = [v for v in variables if v in target_df.columns]
    if not valid_vars:
        raise exceptions.VariableError(
            f"Variables {variables} not found in the dataset."
        )

    return target_df[valid_vars].describe().to_string()


def run_regress(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'regress' command for OLS regression.
    Syntax: regress y x1 x2 x3
    """
    if not HAS_STATSMODELS:
        raise exceptions.DataError(
            "statsmodels is required for regression. Install with: pip install statsmodels"
        )

    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if len(variables) < 2:
        raise exceptions.SyntaxError(
            "regress requires at least 2 variables (dependent and independent)"
        )

    target_df = session.df
    if condition:
        try:
            target_df = session.df.query(condition)
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")

    # First variable is dependent (y), rest are independent (X)
    y_var = variables[0]
    x_vars = variables[1:]

    if y_var not in target_df.columns:
        raise exceptions.VariableError(f"Dependent variable '{y_var}' not found")

    missing_vars = [v for v in x_vars if v not in target_df.columns]
    if missing_vars:
        raise exceptions.VariableError(
            f"Independent variables not found: {missing_vars}"
        )

    # Prepare data
    y = target_df[y_var]
    X = target_df[x_vars]

    # Drop rows with missing values
    data = pd.concat([y, X], axis=1).dropna()
    if len(data) == 0:
        raise exceptions.DataError("No observations after removing missing values")

    y = data[y_var]
    X = data[x_vars]

    # Add constant
    X = sm.add_constant(X)

    # Fit model
    try:
        model = sm.OLS(y, X).fit()
        return model.summary().as_text()
    except Exception as e:
        raise exceptions.DataError(f"Regression failed: {str(e)}")


def run_correlate(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'correlate' command.
    Shows correlation matrix for specified variables or all numeric variables.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    target_df = session.df
    if condition:
        try:
            target_df = session.df.query(condition)
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")

    if not variables:
        # Use all numeric columns
        numeric_df = target_df.select_dtypes(include=["number"])
        if numeric_df.empty:
            raise exceptions.DataError("No numeric variables found")
        return numeric_df.corr().to_string()

    valid_vars = [v for v in variables if v in target_df.columns]
    if not valid_vars:
        raise exceptions.VariableError(
            f"Variables {variables} not found in the dataset."
        )

    return target_df[valid_vars].corr().to_string()
