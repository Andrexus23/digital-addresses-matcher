import pandas as pd
from typing import Dict
from digital_address_matcher.preprocessing.preprocess_manager import PreprocessManager

TYPE_CONFIG_ADDRESSES: Dict = {
    'kladr_1': 'str',
    'kladr_2': 'str',
    'kladr_3': 'str',
    'kladr_4': 'str',
    'kladr_5': 'str',
}

class PreprocessAddressManager(PreprocessManager):
    """Предобработчик таблицы адресов."""
    
    def __init__(self, df_str: str, type_config: Dict = TYPE_CONFIG_ADDRESSES):
        super().__init__(df_str, type_config)
    
    
        
    