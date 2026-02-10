import numpy as np
import pandas as pd
import pytest
from statscrypt.commands.stats import run_correlate, run_regress
from statscrypt.core.exceptions import DataError, SyntaxError, VariableError
from statscrypt.core.session import StatSession


def test_regress_simple():
    """Test simple linear regression."""
    session = StatSession()
    # Create data with known relationship: y = 2*x + 1
    np.random.seed(42)
    x = np.array([1, 2, 3, 4, 5])
    y = 2 * x + 1 + np.random.normal(0, 0.1, 5)
    session.df = pd.DataFrame({"y": y, "x": x})
    session.variables = session.df.columns.tolist()

    result = run_regress(session, ["y", "x"])
    assert "OLS Regression Results" in result
    assert "R-squared" in result
    assert "coef" in result


def test_regress_multiple():
    """Test multiple regression."""
    session = StatSession()
    np.random.seed(42)
    n = 50
    x1 = np.random.randn(n)
    x2 = np.random.randn(n)
    y = 3 + 2 * x1 + 1.5 * x2 + np.random.randn(n) * 0.5

    session.df = pd.DataFrame({"y": y, "x1": x1, "x2": x2})
    session.variables = session.df.columns.tolist()

    result = run_regress(session, ["y", "x1", "x2"])
    assert "OLS Regression Results" in result
    assert "x1" in result
    assert "x2" in result


def test_regress_no_data():
    """Test regress with no data loaded."""
    session = StatSession()
    with pytest.raises(DataError):
        run_regress(session, ["y", "x"])


def test_regress_insufficient_variables():
    """Test regress with insufficient variables."""
    session = StatSession()
    session.df = pd.DataFrame({"y": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(SyntaxError):
        run_regress(session, ["y"])


def test_regress_variable_not_found():
    """Test regress with non-existent variable."""
    session = StatSession()
    session.df = pd.DataFrame({"y": [1, 2, 3], "x": [4, 5, 6]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(VariableError):
        run_regress(session, ["y", "nonexistent"])


def test_correlate_all_variables():
    """Test correlate with all numeric variables."""
    session = StatSession()
    session.df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5], "b": [2, 4, 6, 8, 10], "c": [5, 4, 3, 2, 1]}
    )
    session.variables = session.df.columns.tolist()

    result = run_correlate(session, [])
    assert "a" in result
    assert "b" in result
    assert "c" in result


def test_correlate_specific_variables():
    """Test correlate with specific variables."""
    session = StatSession()
    session.df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5], "b": [2, 4, 6, 8, 10], "c": [5, 4, 3, 2, 1]}
    )
    session.variables = session.df.columns.tolist()

    result = run_correlate(session, ["a", "b"])
    assert "a" in result
    assert "b" in result


def test_correlate_perfect_correlation():
    """Test correlate with perfectly correlated variables."""
    session = StatSession()
    session.df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
    session.variables = session.df.columns.tolist()

    result = run_correlate(session, ["x", "y"])
    # Perfect positive correlation should be 1.0
    assert "1.0" in result or "1.000000" in result


def test_correlate_no_data():
    """Test correlate with no data loaded."""
    session = StatSession()
    with pytest.raises(DataError):
        run_correlate(session, [])


def test_correlate_variable_not_found():
    """Test correlate with non-existent variable."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(VariableError):
        run_correlate(session, ["nonexistent"])
