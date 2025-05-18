"""Адаптируемый класс матчера через aidarmusin/address-ner-ru."""
import torch
from sqlalchemy.orm import Session
from transformers import pipeline
from typing import List, Dict, Tuple, Optional
from transformers.pipelines.base import Pipeline
from digital_address_matcher.common.types import OutputAddressPart, InputAddressPart, EntityPriorities
from digital_address_matcher.address_matcher.abstract_matcher import AbstractMatcher
from digital_address_matcher.services.KladrService import KladrService
from digital_address_matcher.preprocessing.bert_ner_utils.parse_utils import remove_socrs_from_parts_bert
from digital_address_matcher.preprocessing.bert_ner_utils.parse_utils import split_entities_into_parts_bert

class BertMatcher(AbstractMatcher):
    """Адаптируемый класс матчера через aidarmusin/address-ner-ru."""
    
    _model: Optional[Pipeline] = None
    _device: Optional[str] = None
    
    def __init__(self, db_session: Session):
        """Конструктор."""
        self._db_session: Session = db_session
        if BertMatcher._model is None:
            BertMatcher._device = "cuda:0" if torch.cuda.is_available() else "cpu"
            BertMatcher._model = pipeline("ner", model="aidarmusin/address-ner-ru", device=self._device)
            
            
    
    def match(self, addresses: List[str]) -> List[Tuple[List[OutputAddressPart], List[InputAddressPart]]]:
        """Сматчить адрес (специфично для BERT)."""
        parts_entities: List[Dict] = self._model(addresses)
        matched_addresses_list: List[List[OutputAddressPart]] = []
        for address, entities in zip(addresses, parts_entities):
            address_parts: List[InputAddressPart] = split_entities_into_parts_bert(address, entities)
            non_kladr: set = {EntityPriorities.House, EntityPriorities.Apartment, EntityPriorities.Building, EntityPriorities.ZipCode}
            address_parts_kladr: List[InputAddressPart] = list(
                filter(
                    lambda el: el.part_type not in non_kladr,
                    address_parts,
                ),
            )
            address_parts_tail: List[InputAddressPart] = list(
                filter(
                    lambda el: el.part_type in non_kladr,
                    address_parts,
                ),
            )
            address_parts_kladr: List[InputAddressPart] = remove_socrs_from_parts_bert(address_parts_kladr)
            if not address_parts_kladr:
                matched_addresses_list.append(([], []))
                continue
            matched_address: List[OutputAddressPart] = KladrService(self._db_session).get_kladr_codes_by_addr_parts(
                parts=address_parts_kladr,
            )
            matched_addresses_list.append((matched_address, address_parts_tail))
        return matched_addresses_list
            
        
