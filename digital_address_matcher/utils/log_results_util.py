import logging
from typing import List
from digital_address_matcher.common.types import OutputAddressPart

def log_matching_results(matching_results: List[List[OutputAddressPart]], filepath: str = 'logfile.log'):
    logging.basicConfig(filename=filepath, filemode='w', level=logging.DEBUG)
    for matching_result in matching_results:
        try:
            for mathing_item in matching_result:
                logging.info(f'{mathing_item.code}, {mathing_item.parent_code}, {mathing_item.name}, {mathing_item.socr}')
            logging.info('##################################################################')
        except Exception as e:
            logging.error(f'FATAL: {str(e)}')