import pandas as pd
from statscrypt.core.session import StatSession
from typing import List
import statscrypt.core.exceptions as exceptions

def run_summarize(session: StatSession, variables: List[str], condition: str = None):
    """
    Implementation of the 'summarize' command.
    Applies an optional 'if' condition before summarizing.
    """
    if session.df is None:
        raise exceptions.DataError("No data loaded. Use 'use <file.csv>' first.")

    target_df = session.df
    if condition:
        try:
            condition_statement = condition.replace('=', '==')
            target_df = session.df.query(condition_statement)
        except Exception as e:
            raise exceptions.SyntaxError(f"Error in 'if' condition: {e}")
    
    if not variables:
        return target_df.describe().to_string()
    

    valid_vars = [v for v in variables if v in target_df.columns]
    if not valid_vars:
        raise exceptions.VariableError(f"Variables {variables} not found in the dataset.")
        
    return target_df[valid_vars].describe().to_string()
