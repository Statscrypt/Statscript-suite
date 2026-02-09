import pandas as pd
from typing import List, Dict, Any, NamedTuple
import statscrypt.core.exceptions as exceptions

class Token(NamedTuple):
    type: str
    value: str

class StatParser:
    """Simple parser to split Stata command into parts: cmd, vars, and if-clause."""
    
    def parse(self, tokens: List[Token]) -> Dict[str, Any]:
        result = {
            "command": tokens[0].value,
            "variables": [],
            "condition": None
        }
        
        if_index = next((i for i, t in enumerate(tokens) if t.value == 'if'), None)
        
        if result["command"] == "gen":
            if len(tokens) >= 4 and tokens[1].type == 'VAR' and tokens[2].value == '=' and tokens[3].type == 'VAR':
                result["gen_expression"] = {
                    "new_var": tokens[1].value,
                    "operator": tokens[2].value,
                    "old_var": tokens[3].value
                }
                result["variables"] = [] 
            else:
                raise exceptions.SyntaxError("Invalid 'gen' command syntax. Expected 'gen newvar = oldvar'.")
        else:
            if if_index:
                result["variables"] = [t.value for t in tokens[1:if_index]]
            
                result["condition"] = " ".join([t.value for t in tokens[if_index+1:]])
            else:
                result["variables"] = [t.value for t in tokens[1:]]
            
        return result

class Executor:
    def execute(self, session, parsed: Dict):
        df = session.df
        if df is None and parsed["command"] != 'use':
            raise ValueError("No data loaded.")

        target_df = df
        if parsed.get("condition") and df is not None:
            # Basic translation of Stata '==' to Python '=='. A more robust solution is needed for complex cases.
            condition_statement = parsed["condition"].replace('=', '==')
            target_df = df.query(condition_statement)

        # Map commands to functions
        cmd = parsed["command"]
        if cmd == "summarize":
            vars_to_summarize = parsed["variables"] if parsed["variables"] else target_df.columns
            # Filter for variables that actually exist in the dataframe
            valid_vars = [v for v in vars_to_summarize if v in target_df.columns]
            if not valid_vars and parsed["variables"]: 
                 raise ValueError(f"Variables not found: {parsed['variables']}")
            return target_df[valid_vars].describe().to_json()
        
        if cmd == "list":
            return target_df.head(20).to_json()
        
        if cmd == "use":
            filepath = parsed["variables"][0].strip('"')
            session.load_data(filepath)
            return f"Loaded data from {filepath}"

        raise NotImplementedError(f"Command '{cmd}' not implemented.")
