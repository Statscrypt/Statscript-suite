from typing import Optional

import pandas as pd


class StatSession:
    """Manages the current state of the statscrypt environment."""

    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.variables: list[str] = []

    def load_data(self, path: str):
        # For now, we'll use read_csv. The .dta handler will be added later.
        self.df = pd.read_csv(path)
        self.variables = self.df.columns.tolist()

    def get_summary(self):
        if self.df is not None:
            return self.df.describe()
        return "No data loaded."
