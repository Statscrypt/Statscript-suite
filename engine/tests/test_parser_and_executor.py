import pytest
import pandas as pd
from statscrypt.core.session import StatSession
from statscrypt.core.tokenizer import Tokenizer
from statscrypt.core.parser import StatParser
from statscrypt.commands.data_mgmt import run_use, run_list, run_gen
from statscrypt.commands.stats import run_summarize
from statscrypt.commands.viz import run_graph
from statscrypt.core import exceptions
import os
import base64

@pytest.fixture
def session():
    """Pytest fixture to create a StatSession for testing."""
    return StatSession()

@pytest.fixture
def loaded_session(session, tmp_path):
    """Pytest fixture for a session with pre-loaded data."""
    d = tmp_path / "data"
    d.mkdir()
    p = d / "test.csv"
    p.write_text("var1,var2,var_str\n1,2,a\n3,4,b\n5,6,c")
    run_use(session, [f'"{str(p)}"'])
    return session

def test_parser_simple_command():
    """Tests parsing a simple command."""
    tokenizer = Tokenizer()
    parser = StatParser()
    tokens = tokenizer.tokenize("summarize")
    parsed = parser.parse(tokens)
    assert parsed['command'] == 'summarize'
    assert parsed['variables'] == []
    assert parsed['condition'] is None

def test_parser_with_vars_and_condition():
    """Tests parsing a command with variables and an if condition."""
    tokenizer = Tokenizer()
    parser = StatParser()
    tokens = tokenizer.tokenize("list var1 if var2 > 3")
    parsed = parser.parse(tokens)
    assert parsed['command'] == 'list'
    assert parsed['variables'] == ['var1']
    assert parsed['condition'] == 'var2 > 3'

def test_parser_gen_command():
    """Tests parsing a gen command."""
    tokenizer = Tokenizer()
    parser = StatParser()
    tokens = tokenizer.tokenize("gen new_var = var1")
    parsed = parser.parse(tokens)
    assert parsed['command'] == 'gen'
    assert parsed['gen_expression']['new_var'] == 'new_var'
    assert parsed['gen_expression']['old_var'] == 'var1'
    assert parsed['gen_expression']['operator'] == '='

def test_parser_graph_command():
    """Tests parsing a graph command."""
    tokenizer = Tokenizer()
    parser = StatParser()
    tokens = tokenizer.tokenize("graph var1 var2")
    parsed = parser.parse(tokens)
    assert parsed['command'] == 'graph'
    assert parsed['variables'] == ['var1', 'var2']
    assert parsed['condition'] is None

def test_run_use_command(session, tmp_path):
    """Tests loading a file with the 'use' command."""
    p = tmp_path / "sample.csv"
    p.write_text("a,b,c\n1,2,3")
    result = run_use(session, [f'"{str(p)}"'])
    assert "Loaded data" in result
    assert session.df is not None
    assert session.df.shape == (1, 3)

def test_run_summarize_no_data(session):
    """Tests that summarize returns an error if no data is loaded."""
    with pytest.raises(exceptions.DataError, match="r\\(4\\); No data loaded"):
        run_summarize(session, [], condition=None)

def test_run_summarize_all_vars(loaded_session):
    """Tests summarize on all variables."""
    result = run_summarize(loaded_session, [], condition=None)
    assert "var1" in result
    assert "var2" in result
    assert "count" in result
    assert "mean" in result

def test_run_summarize_specific_vars(loaded_session):
    """Tests summarize on a subset of variables."""
    result = run_summarize(loaded_session, ['var1'], condition=None)
    assert "var1" in result
    assert "var2" not in result

def test_run_list_with_condition(loaded_session):
    """Tests the list command with an if condition."""
    result = run_list(loaded_session, [], condition="var1 > 1")
    assert "3" in result
    assert "5" in result
    assert "1" not in result

def test_run_gen_new_var(loaded_session):
    """Tests generating a new variable."""
    initial_vars = loaded_session.variables.copy()
    gen_expression = {"new_var": "var3", "old_var": "var1", "operator": "="}
    result = run_gen(loaded_session, gen_expression)
    assert "Variable 'var3' generated as a copy of 'var1'." in result
    assert "var3" in loaded_session.variables
    assert loaded_session.df['var3'].equals(loaded_session.df['var1'])
    assert len(loaded_session.variables) == len(initial_vars) + 1

def test_run_gen_new_var_exists(loaded_session):
    """Tests generating a variable that already exists."""
    gen_expression = {"new_var": "var1", "old_var": "var2", "operator": "="}
    with pytest.raises(exceptions.VariableError, match="r\\(101\\); Variable 'var1' already exists."):
        run_gen(loaded_session, gen_expression)

def test_run_gen_old_var_not_found(loaded_session):
    """Tests generating a variable from a non-existent old variable."""
    gen_expression = {"new_var": "var3", "old_var": "non_existent_var", "operator": "="}
    with pytest.raises(exceptions.VariableError, match="r\\(101\\); Variable 'non_existent_var' not found in the dataset."):
        run_gen(loaded_session, gen_expression)

def test_run_gen_unsupported_operator(loaded_session):
    """Tests generating a variable with an unsupported operator."""
    gen_expression = {"new_var": "var3", "old_var": "var1", "operator": "+"}
    with pytest.raises(exceptions.SyntaxError, match="r\\(198\\); Unsupported operator '+' for 'gen' command."):
        run_gen(loaded_session, gen_expression)

def test_tokenizer_mismatch_error():
    """Tests that a mismatch token raises a SyntaxError."""
    tokenizer = Tokenizer()
    with pytest.raises(exceptions.SyntaxError, match="r\\(198\\); Unexpected character: @"):
        tokenizer.tokenize("summarize @#$")

def test_parser_invalid_gen_syntax():
    """Tests that invalid 'gen' command syntax raises a SyntaxError."""
    tokenizer = Tokenizer()
    parser = StatParser()
    tokens = tokenizer.tokenize("gen new_var =") # Missing old_var
    with pytest.raises(exceptions.SyntaxError, match="r\\(198\\); Invalid 'gen' command syntax. Expected 'gen newvar = oldvar'."):
        parser.parse(tokens)

def test_run_use_file_not_found(session):
    """Tests that 'use' command raises FileError when file is not found."""
    with pytest.raises(exceptions.FileError, match="r\\(601\\); File not found at non_existent.csv"):
        run_use(session, ['"non_existent.csv"'])

def test_run_summarize_var_not_found(loaded_session):
    """Tests that summarize raises VariableError for non-existent variable."""
    with pytest.raises(exceptions.VariableError, match="r\\(101\\); Variables \\['non_existent'\\] not found in the dataset."):
        run_summarize(loaded_session, ['non_existent'], condition=None)

def test_run_list_var_not_found(loaded_session):
    """Tests that list raises VariableError for non-existent variable."""
    with pytest.raises(exceptions.VariableError, match="r\\(101\\); Variables \\['non_existent'\\] not found."):
        run_list(loaded_session, ['non_existent'], condition=None)

def test_run_list_invalid_condition_syntax(loaded_session):
    """Tests that list raises SyntaxError for invalid 'if' condition."""
    with pytest.raises(exceptions.SyntaxError, match="r\\(198\\); Error in 'if' condition:"):
        run_list(loaded_session, [], condition="var1 > > 5")

def test_run_graph_valid_command(loaded_session):
    """Tests that a valid graph command returns a base64 encoded string."""
    image_base64 = run_graph(loaded_session, ['var1', 'var2'])
    assert isinstance(image_base64, str)
    assert len(image_base64) > 100 # Should be a reasonably long base64 string
    # Try to decode to ensure it's valid base64
    base64.b64decode(image_base64)

def test_run_graph_no_data(session):
    """Tests that graph raises DataError if no data is loaded."""
    with pytest.raises(exceptions.DataError, match="r\\(4\\); No data loaded"):
        run_graph(session, ['var1', 'var2'])

def test_run_graph_too_few_variables(loaded_session):
    """Tests that graph raises SyntaxError for too few variables."""
    with pytest.raises(exceptions.SyntaxError, match="r\\(198\\); Graph command requires exactly two variables: graph var1 var2"):
        run_graph(loaded_session, ['var1'])

def test_run_graph_too_many_variables(loaded_session):
    """Tests that graph raises SyntaxError for too many variables."""
    with pytest.raises(exceptions.SyntaxError, match="r\\(198\\); Graph command requires exactly two variables: graph var1 var2"):
        run_graph(loaded_session, ['var1', 'var2', 'var3'])

def test_run_graph_variable_not_found(loaded_session):
    """Tests that graph raises VariableError for non-existent variables."""
    with pytest.raises(exceptions.VariableError, match="r\\(101\\); Variables 'non_existent' or 'var2' not found in the dataset."):
        run_graph(loaded_session, ['non_existent', 'var2'])
    with pytest.raises(exceptions.VariableError, match="r\\(101\\); Variables 'var1' or 'another_non_existent' not found in the dataset."):
        run_graph(loaded_session, ['var1', 'another_non_existent'])

def test_run_graph_non_numeric_variable(loaded_session):
    """Tests that graph raises DataError for non-numeric variables."""
    with pytest.raises(exceptions.DataError, match="r\\(4\\); Variable 'var_str' is not numeric and cannot be plotted."):
        run_graph(loaded_session, ['var1', 'var_str'])