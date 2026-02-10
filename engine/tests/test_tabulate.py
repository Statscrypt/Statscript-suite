import pandas as pd
import pytest
from statscrypt.commands.stats import run_tabulate
from statscrypt.core.exceptions import DataError, SyntaxError, VariableError
from statscrypt.core.session import StatSession


def test_tabulate_one_way():
    """Test one-way frequency table."""
    session = StatSession()
    session.df = pd.DataFrame({"gender": ["M", "F", "M", "F", "M", "F", "M"]})
    session.variables = session.df.columns.tolist()

    result = run_tabulate(session, ["gender"])
    assert "Freq." in result
    assert "Percent" in result
    assert "Cum." in result
    assert "Total" in result


def test_tabulate_two_way():
    """Test two-way cross-tabulation."""
    session = StatSession()
    session.df = pd.DataFrame(
        {
            "gender": ["M", "F", "M", "F", "M", "F"],
            "region": ["North", "South", "North", "South", "North", "South"],
        }
    )
    session.variables = session.df.columns.tolist()

    result = run_tabulate(session, ["gender", "region"])
    assert "gender x region" in result
    assert "Total" in result


def test_tabulate_numeric():
    """Test tabulate with numeric variable."""
    session = StatSession()
    session.df = pd.DataFrame({"score": [1, 2, 1, 3, 2, 1, 3, 3]})
    session.variables = session.df.columns.tolist()

    result = run_tabulate(session, ["score"])
    assert "Freq." in result
    assert "Total" in result


def test_tabulate_no_variables():
    """Test tabulate with no variables specified."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(SyntaxError):
        run_tabulate(session, [])


def test_tabulate_variable_not_found():
    """Test tabulate with non-existent variable."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(VariableError):
        run_tabulate(session, ["nonexistent"])


def test_tabulate_no_data():
    """Test tabulate with no data loaded."""
    session = StatSession()
    with pytest.raises(DataError):
        run_tabulate(session, ["var"])


def test_tabulate_too_many_variables():
    """Test tabulate with more than 2 variables."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(SyntaxError):
        run_tabulate(session, ["a", "b", "c"])
