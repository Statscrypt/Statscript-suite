import numpy as np
import pandas as pd
import pytest
from statscrypt.commands.data_mgmt import run_gen
from statscrypt.core.exceptions import SyntaxError, VariableError
from statscrypt.core.session import StatSession


def test_gen_arithmetic_addition():
    """Test gen with addition."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "c", "expression": "a + b"})
    assert "c" in session.df.columns
    assert list(session.df["c"]) == [5, 7, 9]


def test_gen_arithmetic_subtraction():
    """Test gen with subtraction."""
    session = StatSession()
    session.df = pd.DataFrame({"revenue": [100, 200, 300], "cost": [40, 80, 120]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "profit", "expression": "revenue - cost"})
    assert list(session.df["profit"]) == [60, 120, 180]


def test_gen_arithmetic_multiplication():
    """Test gen with multiplication."""
    session = StatSession()
    session.df = pd.DataFrame({"price": [10, 20, 30], "quantity": [2, 3, 4]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "total", "expression": "price * quantity"})
    assert list(session.df["total"]) == [20, 60, 120]


def test_gen_arithmetic_division():
    """Test gen with division."""
    session = StatSession()
    session.df = pd.DataFrame({"income": [100, 200, 300], "people": [2, 4, 5]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "per_capita", "expression": "income / people"})
    assert list(session.df["per_capita"]) == [50, 50, 60]


def test_gen_arithmetic_power():
    """Test gen with power operator."""
    session = StatSession()
    session.df = pd.DataFrame({"age": [2, 3, 4]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "age_squared", "expression": "age ** 2"})
    assert list(session.df["age_squared"]) == [4, 9, 16]


def test_gen_function_log():
    """Test gen with log function."""
    session = StatSession()
    session.df = pd.DataFrame({"wage": [np.e, np.e**2, np.e**3]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "log_wage", "expression": "log(wage)"})
    assert np.allclose(session.df["log_wage"], [1, 2, 3])


def test_gen_function_sqrt():
    """Test gen with sqrt function."""
    session = StatSession()
    session.df = pd.DataFrame({"x": [4, 9, 16]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "sqrt_x", "expression": "sqrt(x)"})
    assert list(session.df["sqrt_x"]) == [2, 3, 4]


def test_gen_function_exp():
    """Test gen with exp function."""
    session = StatSession()
    session.df = pd.DataFrame({"x": [0, 1, 2]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "exp_x", "expression": "exp(x)"})
    assert np.allclose(session.df["exp_x"], [1, np.e, np.e**2])


def test_gen_complex_expression():
    """Test gen with complex expression."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "result", "expression": "(a + b) * 2"})
    assert list(session.df["result"]) == [10, 14, 18]


def test_gen_interaction_term():
    """Test gen with interaction term."""
    session = StatSession()
    session.df = pd.DataFrame({"age": [20, 30, 40], "education": [12, 16, 18]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "age_edu", "expression": "age * education"})
    assert list(session.df["age_edu"]) == [240, 480, 720]


def test_gen_variable_not_found():
    """Test gen with non-existent variable."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(Exception):
        run_gen(session, {"new_var": "c", "expression": "a + nonexistent"})


def test_gen_variable_already_exists():
    """Test gen with existing variable name."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(VariableError):
        run_gen(session, {"new_var": "a", "expression": "a + 1"})


def test_gen_with_constant():
    """Test gen with constant value."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    run_gen(session, {"new_var": "b", "expression": "a + 10"})
    assert list(session.df["b"]) == [11, 12, 13]
