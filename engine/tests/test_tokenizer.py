import pytest
from statscrypt.core.exceptions import SyntaxError
from statscrypt.core.tokenizer import Token, Tokenizer


def test_tokenize_simple_command():
    """Tests tokenizing a simple command without arguments."""
    tokenizer = Tokenizer()
    code = "summarize"
    tokens = tokenizer.tokenize(code)
    expected_tokens = [Token("COMMAND", "summarize")]
    assert tokens == expected_tokens


def test_tokenize_command_with_vars():
    """Tests tokenizing a command with variable arguments."""
    tokenizer = Tokenizer()
    code = "summarize age income"
    tokens = tokenizer.tokenize(code)
    expected_tokens = [
        Token("COMMAND", "summarize"),
        Token("VAR", "age"),
        Token("VAR", "income"),
    ]
    assert tokens == expected_tokens


def test_tokenize_use_command_with_string():
    """Tests the 'use' command with a quoted file path."""
    tokenizer = Tokenizer()
    code = 'use "my data/file.csv"'

    tokens = tokenizer.tokenize('use "my data/file.csv"')
    expected_tokens = [Token("COMMAND", "use"), Token("STRING", '"my data/file.csv"')]
    assert tokens == expected_tokens


def test_tokenize_with_if_clause():
    """Tests a command with a conditional 'if' clause."""
    tokenizer = Tokenizer()
    code = "list age if gender == 1"
    tokens = tokenizer.tokenize(code)
    expected_tokens = [
        Token("COMMAND", "list"),
        Token("VAR", "age"),
        Token("IF", "if"),
        Token("VAR", "gender"),
        Token("COMP_OP", "=="),
        Token("NUMBER", "1"),
    ]
    assert tokens == expected_tokens


def test_unexpect_char_raises_error():
    """Tests that an unexpected character raises a SyntaxError."""
    tokenizer = Tokenizer()
    with pytest.raises(SyntaxError):
        tokenizer.tokenize("summarize @#$")
