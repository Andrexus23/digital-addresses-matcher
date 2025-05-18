"""Общие утилиты для упрощения работы."""
import re
from functools import partial
from digital_address_matcher.db.models import Addresses
from typing import Callable, List, Dict
from digital_address_matcher.common.types import LevelEnum, CodeWithLevel, NormalizedKladrHierarchy, OutputAddressPart

UPPER_LEVEL_FIVE_LEN: int = 13

def check_string(allowed_chars: str, string: str) -> bool:
    """Проверка строки на наличие определенных символов. Больше не используется."""
    pattern = f"^[{re.escape(allowed_chars)}]+$"
    return bool(re.match(pattern, string))

def get_level_by_code(code: str) -> int:
    """Определить уровень относительно 1-5 по коду КЛАДР."""
    if not bool(int(code[2:])) and len(code) <= UPPER_LEVEL_FIVE_LEN:
        return LevelEnum.FIRST.value
    if not bool(int(code[5:])) and len(code) <= UPPER_LEVEL_FIVE_LEN:
        return LevelEnum.SECOND.value
    if not bool(int(code[8:])) and len(code) <= UPPER_LEVEL_FIVE_LEN:
        return LevelEnum.THIRD.value
    if not bool(int(code[11:])) and len(code) <= UPPER_LEVEL_FIVE_LEN:
        return LevelEnum.FOURTH.value
    return LevelEnum.FIFTH.value

def from_db_address_to_normalized(address: Addresses) -> NormalizedKladrHierarchy:
    """Приведение к нормализованному виду из таблицы Addresses."""
    return NormalizedKladrHierarchy(
        level_1=CodeWithLevel(
            code=[address.kladr_1],
            level=LevelEnum.FIRST.value,
        ) if address.kladr_1 else None,
        level_2=CodeWithLevel(
            code=[address.kladr_2],
            level=LevelEnum.SECOND.value,
        ) if address.kladr_2 else None,
        level_3=CodeWithLevel(
            code=[address.kladr_3],
            level=LevelEnum.THIRD.value,
        ) if address.kladr_3 else None,
        level_4=CodeWithLevel(
            code=[address.kladr_4],
            level=LevelEnum.FOURTH.value,
        ) if address.kladr_4 else None,
        level_5=CodeWithLevel(
            code=[address.kladr_5],
            level=LevelEnum.FIFTH.value,
        ) if address.kladr_5 else None,
    )
    
def from_actual_codes_to_normalized(codes: List[List[str]]) -> NormalizedKladrHierarchy:
    """Приведение к нормализованному виду из таблицы Addresses."""
    levels: Dict = {
        'level_1': None,
        'level_2': None,
        'level_3': None,
        'level_4': None,
        'level_5': None,    
    }
    for code in codes:
        if not code:
            continue
        level_int: int = get_level_by_code(code[0])
        level_str: str = 'level_' + str(level_int)
        levels[level_str] = CodeWithLevel(
            code=code,
            level=level_int,
        )
    return NormalizedKladrHierarchy(**levels)


def from_output_address_part_to_list(codes: List[OutputAddressPart]) -> List[List[str]]:
    """Для упрощения подсчета f1."""
    actual_list_codes: List = []
    actual_dict_codes: Dict = {}
    for obj in codes:
        if not actual_dict_codes.get(obj.level):
            actual_dict_codes[obj.level] = []
        actual_dict_codes[obj.level].append(obj)
    
    sorted_levels = list(actual_dict_codes.keys())
    sorted_levels.sort()
    for level in sorted_levels:
        actual_list_codes.append([obj.code for obj in actual_dict_codes[level]])
    return actual_list_codes


def from_db_address_to_list(expected: Addresses) -> List[List[str]]:
    """Для упрощения подсчета f1."""
    return list(map(lambda x: [x], filter(lambda x: x is not None, [expected.kladr_1, expected.kladr_2, expected.kladr_3, expected.kladr_4, expected.kladr_5])))
    
            