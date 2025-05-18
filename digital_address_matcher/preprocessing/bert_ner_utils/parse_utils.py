from enum import Enum
from typing import List, Dict, Optional
from digital_address_matcher.preprocessing.socrs import FULL_SOCRS_SET, get_all_socr_variants
from digital_address_matcher.common.types import InputAddressPart, EntityPriorities, OutputAddressPart
        
        
def remove_socrs_from_parts_bert(parts: List[InputAddressPart]) -> List[InputAddressPart]:
    """Удалить socr."""
    def is_socr(start_index, end_index) -> bool:
        return (start_index == 0) or (end_index == (part.part_value.index(part.part_value[-1]) + 1))
    
    for part in parts:
        for socr in FULL_SOCRS_SET:
            found: bool = False
            if socr.lower() in part.part_value.lower():
                socr_variants = get_all_socr_variants(socr)
                for socr_variant in socr_variants:
                    start_index = part.part_value.lower().find(socr_variant.lower())
                    if start_index != -1:
                        end_index = start_index + len(socr_variant)
                        if is_socr(start_index, end_index): 
                            found = True
                            part.part_value = part.part_value.replace(part.part_value[start_index:end_index], '')
                            break
                if found:
                    break
    return parts

def form_address_part_from_list(address: str, entities: list) -> Optional[InputAddressPart]:
    if not entities:
        return None
    object_name: str = address[entities[0]['start']:entities[-1]['end']]
    if EntityPriorities.Region.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.Region)
    elif EntityPriorities.District.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.District)
    elif EntityPriorities.Settlement.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.Settlement)
    elif EntityPriorities.Street.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.Street)
    elif EntityPriorities.ZipCode.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.ZipCode)
    elif EntityPriorities.House.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.House)
    elif EntityPriorities.Building.name in entities[0]['entity']:
         return InputAddressPart(part_value=object_name, part_type=EntityPriorities.Building)
    elif EntityPriorities.Apartment.name in entities[0]['entity']:
        return InputAddressPart(part_value=object_name, part_type=EntityPriorities.Apartment)

def split_entities_into_parts_bert(address: str, entities: List[Dict]) -> List[InputAddressPart]:
    """Разбить список сущностей на части."""
    
    regions: list = []
    districts: list = []
    settlements: list = []
    streets: list = []
    zip_codes: list = []
    houses: list = []
    buildings: list = []
    apartments: list = []
    for entity in entities:
        if EntityPriorities.Region.name in entity['entity']:
            regions.append(entity)
        elif EntityPriorities.District.name in entity['entity']:
            districts.append(entity)
        elif EntityPriorities.Settlement.name in entity['entity']:
            settlements.append(entity)
        elif EntityPriorities.Street.name in entity['entity']:
            streets.append(entity)
        elif EntityPriorities.ZipCode.name in entity['entity']:
            zip_codes.append(entity)
        elif EntityPriorities.House.name in entity['entity']:
            houses.append(entity)
        elif EntityPriorities.Building.name in entity['entity']:
            buildings.append(entity)
        elif EntityPriorities.Apartment.name in entity['entity']:
            apartments.append(entity)

    return list(
        filter(
            lambda el: el is not None,
            [
                form_address_part_from_list(address, regions),
                form_address_part_from_list(address, districts),
                form_address_part_from_list(address, settlements),
                form_address_part_from_list(address, streets),
                form_address_part_from_list(address, zip_codes),
                form_address_part_from_list(address, houses),
                form_address_part_from_list(address, buildings),
                form_address_part_from_list(address, apartments),
            ],
        ),
    )