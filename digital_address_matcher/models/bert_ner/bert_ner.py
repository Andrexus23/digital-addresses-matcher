"""Инициализатор модели BERT."""
import torch
from typing import Optional
from transformers import pipeline
from transformers.pipelines.base import Pipeline
from digital_address_matcher.models.model_initializer.initializer import ModelInitializer

class _BertInitializer(ModelInitializer):
    """Инициализатор BERT-модели."""
    
    def __init__(self):
        """Конструктор."""
        super().__init__()
        self._device: str = ''
        self._model: Optional[Pipeline] = None
        
    def _inner_get_model(self) -> Pipeline:
        """Инициализация BERT-модели."""
        self._device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self._model = pipeline("ner", model="aidarmusin/address-ner-ru", device=self._device)
        return self._model
    
_bert_initializer = _BertInitializer()

def get_bert_ner() -> Pipeline:
    """Получить инстанс трансформера для извлечения частей адреса."""
    return _bert_initializer()
