import pandas as pd
from typing import List, Dict


class PreprocessManager:
    
    def __init__(self, df_str: str, type_config: Dict):
        self.df: pd.DataFrame = pd.read_csv(
            df_str,
            dtype=type_config,
        )
        
    def save(self, path: str):
        self.df.to_csv(path, index=False)