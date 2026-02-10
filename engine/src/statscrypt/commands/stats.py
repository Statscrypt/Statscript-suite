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


def run_tabulate(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'tabulate' command.
    Creates frequency tables for categorical variables.
    Syntax: tabulate var1 [var2]
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if not variables:
        raise exceptions.SyntaxError("tabulate requires at least one variable")

    target_df = session.df
    if condition:
        try:
            target_df = session.df.query(condition)
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")

    var1 = variables[0]
    if var1 not in target_df.columns:
        raise exceptions.VariableError(f"Variable '{var1}' not found")

    if len(variables) == 1:
        # One-way frequency table
        counts = target_df[var1].value_counts().sort_index()
        total = len(target_df)
        percent = (counts / total * 100).round(2)

        result_df = pd.DataFrame(
            {"Freq.": counts, "Percent": percent, "Cum.": percent.cumsum()}
        )

        output = f"\n{var1}\n"
        output += "=" * 50 + "\n"
        output += result_df.to_string()
        output += f"\n{'-' * 50}\n"
        output += f"Total: {total}\n"
        return output

    elif len(variables) == 2:
        # Two-way cross-tabulation
        var2 = variables[1]
        if var2 not in target_df.columns:
            raise exceptions.VariableError(f"Variable '{var2}' not found")

        crosstab = pd.crosstab(
            target_df[var1], target_df[var2], margins=True, margins_name="Total"
        )

        output = f"\n{var1} x {var2}\n"
        output += "=" * 50 + "\n"
        output += crosstab.to_string()
        output += "\n"
        return output

    else:
        raise exceptions.SyntaxError(
            "tabulate supports at most 2 variables (one-way or two-way tables)"
        )


try:
    from scipy import stats as scipy_stats

    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def run_ttest(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'ttest' command.
    Performs t-tests (one-sample or two-sample).
    Syntax: ttest var == value  (one-sample)
            ttest var, by(groupvar)  (two-sample)
    """
    if not HAS_SCIPY:
        raise exceptions.DataError(
            "scipy is required for t-tests. Install with: pip install scipy"
        )

    if session.df is None:
        raise exceptions.DataError("No data loaded.")

    if not variables:
        raise exceptions.SyntaxError("ttest requires a variable")

    target_df = session.df
    if condition:
        try:
            target_df = session.df.query(condition)
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")

    var = variables[0]
    if var not in target_df.columns:
        raise exceptions.VariableError(f"Variable '{var}' not found")

    # Check if it's a comparison (one-sample t-test)
    if len(variables) >= 3 and variables[1] in ["==", "="]:
        try:
            test_value = float(variables[2])
            data = target_df[var].dropna()
            t_stat, p_value = scipy_stats.ttest_1samp(data, test_value)

            output = f"\nOne-sample t-test\n"
            output += "=" * 50 + "\n"
            output += f"Variable: {var}\n"
            output += f"H0: mean = {test_value}\n"
            output += f"Observations: {len(data)}\n"
            output += f"Mean: {data.mean():.4f}\n"
            output += f"Std Dev: {data.std():.4f}\n"
            output += f"t-statistic: {t_stat:.4f}\n"
            output += f"p-value: {p_value:.4f}\n"
            return output
        except ValueError:
            raise exceptions.SyntaxError("Test value must be numeric")

    # Two-sample t-test (by group)
    # This is a simplified version - full implementation would parse "by(var)"
    elif len(variables) == 2:
        group_var = variables[1]
        if group_var not in target_df.columns:
            raise exceptions.VariableError(f"Grouping variable '{group_var}' not found")

        groups = target_df[group_var].unique()
        if len(groups) != 2:
            raise exceptions.DataError(
                f"Two-sample t-test requires exactly 2 groups, found {len(groups)}"
            )

        group1_data = target_df[target_df[group_var] == groups[0]][var].dropna()
        group2_data = target_df[target_df[group_var] == groups[1]][var].dropna()

        t_stat, p_value = scipy_stats.ttest_ind(group1_data, group2_data)

        output = f"\nTwo-sample t-test\n"
        output += "=" * 50 + "\n"
        output += f"Variable: {var}\n"
        output += f"Grouping: {group_var}\n"
        output += f"Group 1 ({groups[0]}): n={len(group1_data)}, mean={group1_data.mean():.4f}\n"
        output += f"Group 2 ({groups[1]}): n={len(group2_data)}, mean={group2_data.mean():.4f}\n"
        output += f"t-statistic: {t_stat:.4f}\n"
        output += f"p-value: {p_value:.4f}\n"
        return output
    else:
        raise exceptions.SyntaxError(
            "ttest syntax: 'ttest var == value' or 'ttest var groupvar'"
        )
