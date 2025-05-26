"""Инициализатор модели Natasha."""
from typing import Optional
from natasha import AddrExtractor, MorphVocab
from digital_address_matcher.models.model_initializer.initializer import ModelInitializer

class _NatashaInitializer(ModelInitializer):
    """Инициализатор Natasha-экстрактора."""
    
    def __init__(self):
        """Конструктор."""
        super().__init__()
        self._morph_vocab: Optional[MorphVocab] = None
        self._extractor: Optional[AddrExtractor] = None
        
    def _inner_get_model(self) -> AddrExtractor:
        """Инициализация Natasha-экстрактора."""
        self._morph_vocab = MorphVocab()
        self._extractor = AddrExtractor(self._morph_vocab)
        return self._extractor
    
_natasha_initializer = _NatashaInitializer()

def get_natasha_extractor() -> AddrExtractor:
    """Получить инстанс Natasha-экстрактора для извлечения частей адреса."""
    return _natasha_initializer()
