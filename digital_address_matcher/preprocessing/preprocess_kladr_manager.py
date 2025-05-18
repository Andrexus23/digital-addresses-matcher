import pandas as pd
from typing import List, Dict
from collections import OrderedDict
from digital_address_matcher.preprocessing.preprocess_manager import PreprocessManager

TYPE_CONFIG_KLADR_BASE: Dict = {
    "index": "Int64",
    "gninmb": "Int64",
    "uno": "Int64",
    "ocatd": "Int64",
    "status": "Int32",
    'code': 'str'
}

TYPE_CONFIG_KLADR_WITH_PARENT_CODES: Dict = {
    "index": "Int64",
    "gninmb": "Int64",
    "uno": "Int64",
    "ocatd": "Int64",
    "status": "Int32",
    'code': 'str',
    'parent_code': 'str',
}



class PreprocessKladrManager(PreprocessManager):
    
    def __init__(self, df_str: str, type_config: Dict):
        super().__init__(df_str, type_config)
        self.existing_codes: set = set(self.df.code)
        
    def get_parent_candidates(self, code) -> List[str]:
        levels = OrderedDict()
        # levels[4] = code[:13]
        levels[3] = code[:11] + '0' * (13 - 11)
        levels[2] = code[:8] + '0' * (13 - 8)
        levels[1] = code[:5] + '0' * (13 - 5)
        levels[0] = code[:2] + '0' * (13 - 2)

        res = OrderedDict()
        for cand in levels.values():
            if cand != code:
                res[cand] = 1
        return list(res.keys())
    
    def find_parent(self, item):
        parent_candidates = self.get_parent_candidates(item['code'])
        for cand in parent_candidates:
            if cand in self.existing_codes:
                return cand
        return None
    
    def delete_non_actual_codes(self):
        """Удаление неактуальных элементов."""
        df = self.df
        self.df = df.loc[df.code.apply(lambda x: x[-2:] == '00')]
    
    def find_sequences(self, parent_field: str = 'parent_code'):
        """Построение цепочек уровней."""
        self.df[parent_field] = self.df.apply(self.find_parent, axis=1)
        
    def change_parent_code(self, old: str, new: str):
        """Поменять parent_code у всех элементов с old на new.

        Args:
            old (_type_): _description_
            new (_type_): _description_
        """
        self.df.loc[self.df['parent_code'] == old, 'parent_code'] = new
        