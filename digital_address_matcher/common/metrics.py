
from typing import List, Dict, Optional, Tuple
from digital_address_matcher.db.models import Addresses
from digital_address_matcher.common.types import OutputAddressPart, InputAddressPart
from digital_address_matcher.common.types import EntityPriorities
from digital_address_matcher.common.utils import from_db_address_to_normalized, from_actual_codes_to_normalized, NormalizedKladrHierarchy, CodeWithLevel
from digital_address_matcher.common.utils import from_output_address_part_to_list, from_db_address_to_list

def compare_zipped_lists_codes(expected_list: List, actual_list: List) -> bool:
    for expected_item, actual_item in zip(expected_list, actual_list):
        if expected_item == actual_item:
            continue
        if not set(expected_item).intersection(set(actual_item)):
            return False
    return True
            

def calculate_tp_strict(expected_list: List, actual_list: List) -> bool:
    """Вычисление TP строгим путем - количество уровней кладр expected и actual должны совпадать.

    Args:
        expected_list (List): ожидаемый список
        actual_list (List): фактический список

    Returns:
        bool: Результат сравнения.
    """
    if not actual_list:
        return False
    if len(actual_list) != len(expected_list):
        return False
    else:
        return compare_zipped_lists_codes(expected_list, actual_list)


def calculate_tp_soft(expected_list: List, actual_list: List) -> bool:
    """Вычисление TP мягким путем - expected_list обязан быть подмножеством actual_list в единой последовательности сверху вниз."""
    if not actual_list:
        return False
    return compare_zipped_lists_codes(expected_list, actual_list)

def init_TP_FP_TN_FN():
    return {
        'TP': 0,
        'FP': 0,
        'TN': 0,
        'FN': 0,
    }



def calculate_metrics_for_one_level(expected: List[str], actual: List[str], level_map: Dict):
    if expected and set(expected).intersection(set(actual)):
        level_map['TP'] += 1
    elif actual and not set(expected).intersection(set(actual)):
        level_map['FP'] += 1
    elif not actual and expected:
        level_map['FN'] += 1

        
def calculate_metrics_for_one_level_none_case(
    expected: Optional[List[str]], actual: Optional[List[str]], level_map: Dict,
):
    if expected is None and actual is None:
        level_map['TN'] += 1
    elif expected is None and actual is not None:
        level_map['FP'] += 1
    elif expected is not None and actual is None:
        level_map['FN'] += 1

def calculate_metrics_by_levels(expected: NormalizedKladrHierarchy, actual: NormalizedKladrHierarchy, TP_FP_TN_FN_DICT_LEVELS: Dict):
    """Подсчитать метрики по уровням."""
    for key, expected_lvl, actual_lvl in zip(
        ['level_1',  'level_2',  'level_3',  'level_4',  'level_5'],
        [expected.level_1, expected.level_2, expected.level_3, expected.level_4, expected.level_5],
        [actual.level_1, actual.level_2, actual.level_3, actual.level_4, actual.level_5],
    ):
        if expected_lvl is None or actual_lvl is None:
            calculate_metrics_for_one_level_none_case(expected_lvl, actual_lvl, TP_FP_TN_FN_DICT_LEVELS[key])
            continue
            
        try:
            calculate_metrics_for_one_level(expected_lvl.code, actual_lvl.code, TP_FP_TN_FN_DICT_LEVELS[key])
        except Exception as e:
            print(f'Error: {e}')



def calculate_states(expected_objects: List[Addresses], actual_objects: List[OutputAddressPart], strict_mode: bool = True, consider_levels: bool = True, log_only_errors: bool = True):
    """Получить TP, TN, FP."""
    errors = []
    TP_FP_TN_FN_DICT_LEVELS: Dict = {
        'level_1': init_TP_FP_TN_FN(),
        'level_2': init_TP_FP_TN_FN(),
        'level_3': init_TP_FP_TN_FN(),
        'level_4': init_TP_FP_TN_FN(),
        'level_5': init_TP_FP_TN_FN(),
    } if consider_levels else {}
    TP, FP, TN, FN = 0, 0, 0, 0
    for expected, actual in zip(expected_objects, actual_objects):
        
        expected_list_codes: List = from_db_address_to_list(expected)
        actual_list_codes: List[List[str]] = from_output_address_part_to_list(actual)
        normalized_expected: NormalizedKladrHierarchy = from_db_address_to_normalized(expected)
        normalized_actual: NormalizedKladrHierarchy = from_actual_codes_to_normalized(actual_list_codes)
        if consider_levels:
            calculate_metrics_by_levels(normalized_expected, normalized_actual, TP_FP_TN_FN_DICT_LEVELS)

        IS_TP: bool = calculate_tp_strict(expected_list_codes, actual_list_codes) if strict_mode else calculate_tp_soft(expected_list_codes, actual_list_codes)
        
        if IS_TP and actual_list_codes:
            TP += 1
            continue
        elif actual_list_codes and (actual_list_codes != expected_list_codes):
            FP += 1
            errors.append((expected, actual))
        elif (actual_list_codes == expected_list_codes) and not actual_list_codes:
            TN += 1
        elif not actual_list_codes and expected_list_codes:
            FN +=1
            errors.append((expected, actual))
        # print(f'ERROR: address_id: {expected.addresses_id}: {expected_list_codes} {actual_list_codes}')
        
    return TP, FP, TN, FN, TP_FP_TN_FN_DICT_LEVELS, errors


def f1_score(TP, FP, TN, FN):
    return 2*TP / (2*TP + FP + FN)


def accuracy(TP, FP, TN, FN):
    return (TP+TN) / (TP + TN + FP + FN)


def fdr(TP, FP, TN, FN):
    return FP / (TP + FP)


def calculate_states_strs(expected: str, actual: List[str], states_map: Dict):
    """"""
    if actual and expected and (expected in actual[0]):
        states_map['TP'] += 1
    elif (actual and not expected) or ((actual and expected) and (expected not in actual[0])):
        states_map['FP'] += 1
    elif not actual and not expected:
        states_map['TN'] += 1
    elif not actual and expected:
        states_map['FN'] += 1
    


def calculate_states_for_zipcode(expected: Addresses, actual_seq: List[InputAddressPart], states_map: Dict):
    """"""
    actual = list(map(lambda x: x.part_value, filter(lambda x: x.part_type == EntityPriorities.ZipCode, actual_seq)))
    calculate_states_strs(expected.post_index, actual, states_map)
        
    
def calculate_states_for_building(expected: Addresses, actual_seq: List[InputAddressPart], states_map: Dict):
    """"""
    actual = list(map(lambda x: x.part_value, filter(lambda x: x.part_type == EntityPriorities.Building, actual_seq)))
    calculate_states_strs(expected.building, actual, states_map)
    
def calculate_states_for_house(expected: Addresses, actual_seq: List[InputAddressPart], states_map: Dict):
    """"""
    actual = list(map(lambda x: x.part_value, filter(lambda x: x.part_type == EntityPriorities.House, actual_seq)))
    calculate_states_strs(expected.house, actual, states_map)
    
def calculate_states_for_apartment(expected: Addresses, actual_seq: List[InputAddressPart], states_map: Dict):
    """"""
    actual = list(map(lambda x: x.part_value, filter(lambda x: x.part_type == EntityPriorities.Apartment, actual_seq)))
    calculate_states_strs(expected.flat, actual, states_map)
    
def calculate_states_non_kladr_common(expected: Addresses, actual: List[InputAddressPart], states_map: Dict):
    actual_seq = list(filter(lambda x: x.part_type in {
        EntityPriorities.ZipCode, EntityPriorities.House, EntityPriorities.Building, EntityPriorities.Apartment,
    }, actual))
    actual_seq = sorted(actual_seq, key=lambda x: x.part_type.value)
    actual_seq = list(map(lambda x: x.part_value, actual_seq))
    expected_seq = list(filter(lambda x: x is not None, [expected.post_index, expected.house, expected.building, expected.flat]))
    
    if actual_seq and len(actual_seq) == len(expected_seq):
        OK = True
        for a, e in zip(actual_seq, expected_seq):
            if e not in a:
                OK = False
                states_map['FP'] += 1
                break
        if OK:
            states_map['TP'] += 1
    elif actual_seq and len(actual_seq) != len(expected_seq):
        states_map['FP'] += 1
    elif not actual_seq and not expected_seq:
        states_map['TN'] += 1
    elif not actual_seq and expected_seq:
        states_map['FN'] += 1

    
    


def calculate_states_non_kladr(expected_objects: List[Addresses], actual_objects: List[List[InputAddressPart]]) -> Tuple[Dict, Dict]:
    """Получить TP_FP_TN_FN для не КЛАДР-объектов."""
    errors = []
    TP_FP_TN_FN_DICT: Dict = {
        'zipcode': init_TP_FP_TN_FN(),
        'house': init_TP_FP_TN_FN(),
        'building': init_TP_FP_TN_FN(),
        'apartment': init_TP_FP_TN_FN(),
    }
    TP_FP_TN_FN_COMMON = init_TP_FP_TN_FN()
    for expected, actual_seq in zip(expected_objects, actual_objects):
        calculate_states_non_kladr_common(expected, actual_seq, TP_FP_TN_FN_COMMON)
        calculate_states_for_zipcode(expected, actual_seq, TP_FP_TN_FN_DICT['zipcode'])
        calculate_states_for_house(expected, actual_seq, TP_FP_TN_FN_DICT['house'])
        calculate_states_for_building(expected, actual_seq, TP_FP_TN_FN_DICT['building'])
        calculate_states_for_apartment(expected, actual_seq, TP_FP_TN_FN_DICT['apartment'])
    return TP_FP_TN_FN_COMMON, TP_FP_TN_FN_DICT