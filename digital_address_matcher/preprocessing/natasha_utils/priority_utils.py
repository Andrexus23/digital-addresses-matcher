from typing import List
from natasha.grammars.addr import AddrPart
from digital_address_matcher.preprocessing.socrs import Priority, PRIORITY_MAP
from digital_address_matcher.common.types import InputAddressPart, EntityPriorities

def set_addr_part_priority(fact: AddrPart):
    for prio in PRIORITY_MAP:
        if fact.type in PRIORITY_MAP[prio]:
            return prio
    return Priority.LATEST
    

def get_sorted_matches(matches: List[AddrPart]) -> List[AddrPart]:
    """Cортирует в порядке увеличения приоритета. Возвращает отсортированный список частей адреса."""
    address_sorted_parts: List[AddrPart] = list([(match, set_addr_part_priority(match)) for match in matches])
    address_sorted_parts.sort(key=lambda t: t[1])
    return [part[0] for part in address_sorted_parts if part[1] != Priority.LATEST]

def get_parts_in_normalized_format(parts: List[AddrPart]) -> List[InputAddressPart]:
    """Получить части в нормализованном формате."""
    result_list: List[InputAddressPart] = []

    for part in parts:
        for key in PRIORITY_MAP:
            if part.type in PRIORITY_MAP[key]:
                if key == Priority.FIRST:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.Region))
                elif key == Priority.SECOND:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.District))
                elif key == Priority.THIRD:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.Settlement))
                elif key == Priority.FIFTH:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.Street))
                elif key == Priority.SIXTH:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.ZipCode))
                elif key == Priority.SEVENTH:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.House))
                elif key == Priority.EIGHTH:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.Building))
                elif key == Priority.NINTH:
                    result_list.append(InputAddressPart(part_value=part.value, part_type=EntityPriorities.Apartment))

    return result_list

