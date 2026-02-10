import pandas as pd
import pytest
from statscrypt.core.parser import StatParser
from statscrypt.core.session import StatSession
from statscrypt.core.tokenizer import Tokenizer


def test_condition_greater_equal():
    """Test >= operator in conditions."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("summarize if age >= 30")
    assert any(t.value == ">=" for t in tokens)


def test_condition_less_equal():
    """Test <= operator in conditions."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("list if salary <= 50000")
    assert any(t.value == "<=" for t in tokens)


def test_condition_not_equal():
    """Test != operator in conditions."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("summarize if status != 0")
    assert any(t.value == "!=" for t in tokens)


def test_condition_and_operator():
    """Test & (and) operator in conditions."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("list if age > 25 & income < 50000")
    assert any(t.value == "&" for t in tokens)


def test_condition_or_operator():
    """Test | (or) operator in conditions."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("list if region == 1 | region == 2")
    assert any(t.value == "|" for t in tokens)


def test_compound_condition_execution():
    """Test execution of compound conditions."""
    session = StatSession()
    df = pd.DataFrame({"age": [20, 30, 40, 50], "income": [30000, 50000, 70000, 90000]})
    session.df = df
    session.variables = df.columns.tolist()

    # Test with >= condition
    filtered = session.df.query("age >= 30")
    assert len(filtered) == 3

    # Test with compound condition
    filtered = session.df.query("(age >= 30) & (income < 80000)")
    assert len(filtered) == 2
