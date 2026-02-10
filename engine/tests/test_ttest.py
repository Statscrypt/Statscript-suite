import numpy as np
import pandas as pd
import pytest
from statscrypt.commands.stats import run_ttest
from statscrypt.core.exceptions import DataError, SyntaxError, VariableError
from statscrypt.core.session import StatSession


def test_ttest_one_sample():
    """Test one-sample t-test."""
    session = StatSession()
    np.random.seed(42)
    # Generate data with mean around 50
    data = np.random.normal(50, 10, 30)
    session.df = pd.DataFrame({"score": data})
    session.variables = session.df.columns.tolist()

    result = run_ttest(session, ["score", "==", "50"])
    assert "One-sample t-test" in result
    assert "t-statistic" in result
    assert "p-value" in result


def test_ttest_two_sample():
    """Test two-sample t-test."""
    session = StatSession()
    np.random.seed(42)
    group1 = np.random.normal(50, 10, 20)
    group2 = np.random.normal(55, 10, 20)
    session.df = pd.DataFrame(
        {
            "score": np.concatenate([group1, group2]),
            "group": ["A"] * 20 + ["B"] * 20,
        }
    )
    session.variables = session.df.columns.tolist()

    result = run_ttest(session, ["score", "group"])
    assert "Two-sample t-test" in result
    assert "Group 1" in result
    assert "Group 2" in result


def test_ttest_no_data():
    """Test ttest with no data loaded."""
    session = StatSession()
    with pytest.raises(DataError):
        run_ttest(session, ["var", "==", "0"])


def test_ttest_variable_not_found():
    """Test ttest with non-existent variable."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(VariableError):
        run_ttest(session, ["nonexistent", "==", "0"])


def test_ttest_no_variable():
    """Test ttest without variable."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(SyntaxError):
        run_ttest(session, [])
