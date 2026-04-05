from typing import Any, Dict, List, NamedTuple

import pandas as pd
import statscrypt.core.exceptions as exceptions


class Token(NamedTuple):
    type: str
    value: str


class StatParser:
    """Simple parser to split Stata command into parts: cmd, vars, and if-clause."""

    def parse(self, tokens: List[Token]) -> Dict[str, Any]:
        result = {"command": tokens[0].value, "variables": [], "condition": None}

        if_index = next((i for i, t in enumerate(tokens) if t.value == "if"), None)

        if result["command"] == "gen":
            if (
                len(tokens) >= 4
                and tokens[1].type == "VAR"
                and tokens[2].value in ["=", "=="]
            ):
                # Find where the expression starts (after =)
                expr_start = 3
                expr_end = if_index if if_index else len(tokens)

                # Extract expression tokens
                expr_tokens = tokens[expr_start:expr_end]
                expression = " ".join([t.value for t in expr_tokens])

                result["gen_expression"] = {
                    "new_var": tokens[1].value,
                    "expression": expression,
                }
                result["variables"] = []

                # Handle if condition for gen
                if if_index:
                    result["condition"] = self._parse_condition(tokens[if_index + 1 :])
            else:
                raise exceptions.SyntaxError(
                    "Invalid 'gen' command syntax. Expected 'gen newvar = expression'."
                )
        else:
            if if_index:
                result["variables"] = [t.value for t in tokens[1:if_index]]
                result["condition"] = self._parse_condition(tokens[if_index + 1 :])
            else:
                result["variables"] = [t.value for t in tokens[1:]]

        return result

    def _parse_condition(self, tokens: List[Token]) -> str:
        """Parse condition tokens into pandas query string."""
        condition_parts = []
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token.type == "VAR":
                condition_parts.append(f"{token.value}")
            elif token.type == "COMP_OP":
                # Convert = to ==
                op = token.value if token.value != "=" else "=="
                condition_parts.append(op)
            elif token.type == "LOGIC_OP":
                condition_parts.append(token.value)
            elif token.type == "NUMBER":
                condition_parts.append(token.value)
            elif token.type == "STRING":
                condition_parts.append(token.value)

            i += 1

        return " ".join(condition_parts)


class Executor:
    def execute(self, session, parsed: Dict):
        df = session.df
        if df is None and parsed["command"] != "use":
            raise ValueError("No data loaded.")

        target_df = df
        if parsed.get("condition") and df is not None:
            # Basic translation of Stata '==' to Python '=='. A more robust solution is needed for complex cases.
            condition_statement = parsed["condition"].replace("=", "==")
            target_df = df.query(condition_statement)

        cmd = parsed["command"]
        if cmd == "summarize":
            vars_to_summarize = (
                parsed["variables"] if parsed["variables"] else target_df.columns
            )

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
