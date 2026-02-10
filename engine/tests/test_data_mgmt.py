import os
import tempfile

import pandas as pd
import pytest
from statscrypt.commands.data_mgmt import run_count, run_drop, run_keep, run_save
from statscrypt.core.exceptions import DataError, SyntaxError, VariableError
from statscrypt.core.session import StatSession


def test_drop_variables():
    """Test dropping variables."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    session.variables = session.df.columns.tolist()

    result = run_drop(session, ["b", "c"])
    assert "a" in session.df.columns
    assert "b" not in session.df.columns
    assert "c" not in session.df.columns


def test_drop_observations():
    """Test dropping observations with condition."""
    session = StatSession()
    session.df = pd.DataFrame({"age": [20, 30, 40, 50]})
    session.variables = session.df.columns.tolist()

    result = run_drop(session, [], condition="age < 30")
    assert len(session.df) == 3
    assert session.df["age"].min() == 30


def test_keep_variables():
    """Test keeping specific variables."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    session.variables = session.df.columns.tolist()

    result = run_keep(session, ["a", "b"])
    assert "a" in session.df.columns
    assert "b" in session.df.columns
    assert "c" not in session.df.columns


def test_keep_observations():
    """Test keeping observations with condition."""
    session = StatSession()
    session.df = pd.DataFrame({"age": [20, 30, 40, 50]})
    session.variables = session.df.columns.tolist()

    result = run_keep(session, [], condition="age >= 30")
    assert len(session.df) == 3
    assert session.df["age"].min() == 30


def test_save_csv():
    """Test saving data to CSV."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    session.variables = session.df.columns.tolist()

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        filepath = f.name

    try:
        result = run_save(session, [filepath])
        assert os.path.exists(filepath)

        # Verify saved data
        loaded = pd.read_csv(filepath)
        assert list(loaded.columns) == ["a", "b"]
        assert len(loaded) == 3
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


def test_count_all():
    """Test counting all observations."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    session.variables = session.df.columns.tolist()

    result = run_count(session, [])
    assert result == "5"


def test_count_with_condition():
    """Test counting with condition."""
    session = StatSession()
    session.df = pd.DataFrame({"age": [20, 30, 40, 50, 60]})
    session.variables = session.df.columns.tolist()

    result = run_count(session, [], condition="age >= 40")
    assert result == "3"


def test_drop_no_data():
    """Test drop with no data loaded."""
    session = StatSession()
    with pytest.raises(DataError):
        run_drop(session, ["a"])


def test_keep_variable_not_found():
    """Test keep with non-existent variable."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(VariableError):
        run_keep(session, ["nonexistent"])


def test_save_no_filename():
    """Test save without filename."""
    session = StatSession()
    session.df = pd.DataFrame({"a": [1, 2, 3]})
    session.variables = session.df.columns.tolist()

    with pytest.raises(SyntaxError):
        run_save(session, [])
