
import itertools
import pandas as pd
from typing import List, Tuple
from natasha import AddrExtractor
from natasha.grammars.addr import AddrPart
from digital_address_matcher.preprocessing.socrs import KLADR_SOCRS_STR

FORBIDDEN_TOKENS: List[str] = ['']
PARSE_UNTIL_NUMBER: int = 0
MIN_PART_LENGTH: int = 2

def get_unique_socr(df: pd.DataFrame):
    """Получить все обозначения socr."""
    return set(df.socr.unique())


def split_address_into_parts_by(addr: str, by: str = ', ') -> List[List[str]]:
    """Разбить адрес на части при помощи определенного символа."""
    addr_list = addr.split(by)
    for i in range(len(addr_list)):
        addr_list[i] = addr_list[i].split('. ')
        addr_list[i] = list(filter(lambda x: x not in FORBIDDEN_TOKENS, addr_list[i]))
    return addr_list



def extract_addr_parts_from_parts(parts: List[List[str]], extractor: AddrExtractor) -> Tuple[List[AddrPart], List]:
    """
    Получение нормализованных Natash-ей частей адреса из токенизированных ненормализованных частей при помощи парсинга различных перестановок. 
    Args:
        parts (List[List[str]]): токенизированные части адреса разных уровней в виде списка списков строк
        extractor (AddrExtractor): экстрактор Natasha
    """
    tail: List = []
    natasha_parts: List[AddrPart] = []
    while (len(parts) > PARSE_UNTIL_NUMBER):
        part = parts[0]
        permutations = list(itertools.permutations(part))
        found: bool = False
        for perm in permutations:
            matches_list: List[AddrPart] = [m.fact for m in list(extractor(' '.join(perm)))]
            if not matches_list:
                continue
            new_match = matches_list[0]
        
            if new_match.value not in perm:
                perm = sorted(filter(lambda x: x.strip(',.').lower() not in KLADR_SOCRS_STR.lower(), perm), key=len, reverse=True)
                if not perm:
                    continue
                new_match.value = perm[0] 
                       
            natasha_parts.append(new_match)
            found = True
            break
    
        part = parts.pop(0)
        if not found:
            tail.append(part)
    return natasha_parts, tail
    
    