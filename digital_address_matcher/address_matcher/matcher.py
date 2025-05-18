"""Главный класс матчер, аггрегирующий в себя работу с моделями."""
from typing import List, Dict
from sqlalchemy.orm import Session
from digital_address_matcher.common.types import OutputAddressPart, ModelEnum
from digital_address_matcher.address_matcher.bert_ner_matcher import BertMatcher
from digital_address_matcher.address_matcher.natasha_matcher import NatashaMatcher

_model_cases: Dict = {
    ModelEnum.BERT_NER_CASE: BertMatcher,
    ModelEnum.NATASHA_CASE: NatashaMatcher,
}

class AddressMatcher:
    
    def __init__(self, db_session: Session):
        """Конструктор."""
        self._db_session: Session = db_session
        
    def match(self, addresses: List[str], model_case: ModelEnum = ModelEnum.BERT_NER_CASE) -> List[List[OutputAddressPart]]:
        """Матчинг адреса и выдача результата."""
        try:
            matcher = _model_cases[model_case]
        except KeyError:
            raise ValueError('Некорректный тип модели')
        
        return matcher(self._db_session).match(addresses)

            