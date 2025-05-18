import sys, os
import pytest
from typing import List, Tuple, Dict
from natasha import AddrExtractor, MorphVocab
from natasha.grammars.addr import AddrPart
from digital_address_matcher.preprocessing.natasha_utils.priority_utils import get_sorted_matches
from digital_address_matcher.preprocessing.natasha_utils.parse_utils import extract_addr_parts_from_parts, split_address_into_parts_by

morph_vocab = MorphVocab()
extractor = AddrExtractor(morph_vocab)

@pytest.mark.parametrize("address", [
    "352330, край. Краснодарский, р-н. Усть-Лабинский, г. Усть-Лабинск, ул. Красноармейская, д. 160, кв. 11",
    "187556, обл. Ленинградская, р-н. Тихвинский, г. Тихвин, мкр. 6, д. 29, кв. 85", 
    "180503, обл. Псковская, р-н. Псковский, д. Дуброво, ул. Окольная, д. 1, кв. 103", 
])
def test_sorting(address: str):
    parts = split_address_into_parts_by(address)
    normalized_parts, tail = extract_addr_parts_from_parts(parts,  extractor)
    parts_list: List[Tuple[AddrPart, int]] = get_sorted_matches(normalized_parts)
    kladr_codes_map: Dict[str, AddrPart] = {}
    print(parts_list, tail)
    
    
    