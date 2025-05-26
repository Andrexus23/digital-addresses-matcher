"""Адаптируемый класс матчера через natasha."""
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from natasha import AddrExtractor, MorphVocab
from digital_address_matcher.models.natasha.get_natasha import get_natasha_extractor
from digital_address_matcher.services.KladrService import KladrService
from digital_address_matcher.common.types import InputAddressPart, OutputAddressPart, EntityPriorities
from digital_address_matcher.address_matcher.abstract_matcher import AbstractMatcher
from digital_address_matcher.preprocessing.natasha_utils.priority_utils import get_sorted_matches
from digital_address_matcher.preprocessing.natasha_utils.priority_utils import get_parts_in_normalized_format
from digital_address_matcher.preprocessing.natasha_utils.parse_utils import extract_addr_parts_from_parts, split_address_into_parts_by

class NatashaMatcher(AbstractMatcher):
    """Адаптируемый класс матчера через natasha."""
    
    def __init__(self, db_session: Session):
        """Конструктор."""
        self._db_session: Session = db_session
    
    def match(self, addresses: List[str]) -> List[Tuple[List[OutputAddressPart], List[InputAddressPart]]]:
        """Сматчить адрес (специфично для natasha)."""
        natasha_extractor: AddrExtractor = get_natasha_extractor()
        matched_addresses_list: List[List[OutputAddressPart]] = []
        for address in addresses:
            parts = split_address_into_parts_by(address)
            normalized_parts, tail = extract_addr_parts_from_parts(parts,  natasha_extractor)
            parts_list: List[AddrPart] = get_sorted_matches(normalized_parts)
            parts_list: List[InputAddressPart] = get_parts_in_normalized_format(parts_list)
            
            tail: List = list(
                filter(
                    lambda x: x.part_type in {EntityPriorities.House, EntityPriorities.Apartment, EntityPriorities.Building, EntityPriorities.ZipCode},
                    get_parts_in_normalized_format([part.fact for part in natasha_extractor(address)]),
                ),
            )

            if not parts_list:
                matched_addresses_list.append(([], []))
                continue
            matched_address: List[OutputAddressPart] = KladrService(self._db_session).get_kladr_codes_by_addr_parts(
                parts=parts_list,
            )
            matched_addresses_list.append((matched_address, tail))
        return matched_addresses_list
            
        
