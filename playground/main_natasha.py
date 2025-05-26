import sys
import time
sys.path.append('/home/andrey/github-release/digital-addresses-matcher')
from sqlalchemy.orm import Session
from digital_address_matcher.address_matcher.matcher import AddressMatcher
from digital_address_matcher.db.base import engine
from digital_address_matcher.db.models import Addresses
from digital_address_matcher.services.AddressService import AddressService
from digital_address_matcher.common.types import OutputAddressPart, ModelEnum
from digital_address_matcher.utils.log_results_util import log_matching_results
from digital_address_matcher.common.metrics import calculate_states, f1_score, accuracy, fdr, calculate_states_non_kladr

with Session(bind=engine) as session:
    addresses = AddressService(session).get_addresses_where(limit=100)
    addresses_strs = [addr.epgu_address for addr in addresses]
    # addresses_strs = ['194156, г. Санкт-Петербург, пр-кт. Большой Сампсониевский, д. 85, к. 1, кв. 26']
    matcher = AddressMatcher(session)
    start_time = time.time()
    parsed_addresses_with_tails = matcher.match(addresses_strs, model_case=ModelEnum.NATASHA_CASE)
    end_time = time.time()
    parsed_addresses = list(map(lambda x: x[0], parsed_addresses_with_tails))
    tails = list(map(lambda x: x[1], parsed_addresses_with_tails))
    TP, FP, TN, FN, TP_FP_TN_FN_DICT_LEVELS, errors_list = calculate_states(addresses, parsed_addresses)
    
    print(f'Time spent: {end_time - start_time} s')
    log_matching_results(parsed_addresses)

    print('-----Strict mode----')
    TP, FP, TN, FN, TP_FP_TN_FN_DICT_LEVELS, errors_list = calculate_states(addresses, parsed_addresses, log_only_errors=False, strict_mode=True)
    # print(f'Errors list ids: {[error[0].addresses_id for error in errors_list]}')
    print(len(addresses), sum([TP, FP, TN, FN]))

    print('Common: ')
    print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
    print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
    print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')    

    print('-----Soft mode----')
    TP, FP, TN, FN, _, errors_list = calculate_states(addresses, parsed_addresses, log_only_errors=False, consider_levels=False, strict_mode=False)
    # print(f'Errors list ids: {[error[0].addresses_id for error in errors_list]}')
    print(len(addresses), sum([TP, FP, TN, FN]))

    print('Common: ')
    print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
    print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
    print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
    # parsed_addresses = matcher.match(addresses, model_case=ModelEnum.NATASHA_CASE)
    # parsed_addresses = matcher.match(addresses, model_case=ModelEnum.NATASHA_CASE)
    print('----------------------------')
    print('By levels: ')
    for level in TP_FP_TN_FN_DICT_LEVELS:
        print(level)
        TP = TP_FP_TN_FN_DICT_LEVELS[level]['TP']
        FP = TP_FP_TN_FN_DICT_LEVELS[level]['FP']
        TN = TP_FP_TN_FN_DICT_LEVELS[level]['TN']
        FN = TP_FP_TN_FN_DICT_LEVELS[level]['FN']
        print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
        print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
        print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
        
    print('----------------------------')
    print('For Non-KLADR:')
    parsed_tails = list(map(lambda x: x[1], parsed_addresses_with_tails))
    TP_FP_TN_FN_NON_KLADR_COMMON, TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT = calculate_states_non_kladr(addresses, parsed_tails)
    TP = TP_FP_TN_FN_NON_KLADR_COMMON['TP']
    FP = TP_FP_TN_FN_NON_KLADR_COMMON['FP']
    TN = TP_FP_TN_FN_NON_KLADR_COMMON['TN']
    FN = TP_FP_TN_FN_NON_KLADR_COMMON['FN']
    print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
    print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
    print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
    print('----------------------------')
    print('Index:')
    current_component = 'zipcode'
    TP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TP']
    FP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FP']
    TN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TN']
    FN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FN']
    print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
    print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
    print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
    print('----------------------------')
    print('House:')
    current_component = 'house'
    TP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TP']
    FP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FP']
    TN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TN']
    FN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FN']
    print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
    print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
    print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
    print('----------------------------')
    try:
        print('Building:')
        current_component = 'building'
        TP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TP']
        FP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FP']
        TN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TN']
        FN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FN']
        print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
        print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
        print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
        print('----------------------------')
    except ZeroDivisionError:
        pass
    print('Apartment:')
    current_component = 'apartment'
    TP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TP']
    FP = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FP']
    TN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['TN']
    FN = TP_FP_TN_FN_DICT_ZIPCODE_HOUSE_BUILDING_APARTMENT[current_component]['FN']
    print(f'F1-score: {f1_score(TP, FP, TN, FN)}')
    print(f'False Discovery Rate: {fdr(TP, FP, TN, FN)}')
    print(f'Accuracy: {accuracy(TP, FP, TN, FN)}')
    print('----------------------------')
