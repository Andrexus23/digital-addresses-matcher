from typing import List, Dict
from pydantic import BaseModel
from digital_address_matcher.common.types import OutputAddressPart, InputAddressPart
from digital_address_matcher.common.utils import get_level_by_code

class ApiAddressPart(BaseModel):
    """Базовая модель API для разобранного адреса."""
    name: str

class ApiKladrAddressPart(ApiAddressPart):
    """API представление КЛАДР-объектов."""
    code: str
    socr: str
    level: int
    
class ApiTailAddressPart(ApiAddressPart):
    """API представление НЕ КЛАДР-объектов."""
    type: str

    
def parsed_address_to_api(kladr_part: List[OutputAddressPart], tail_part: List[InputAddressPart]):
    """Преобразование разобранных адресов в формат API."""
    result_seq: List[ApiAddressPart | ApiKladrAddressPart | ApiTailAddressPart] = []
    for part in kladr_part:
        result_seq.append(
            ApiKladrAddressPart(
                code=part.code,
                name=part.name,
                socr=part.socr,
                level=get_level_by_code(part.code),
            ),
        )
    
    for part in tail_part:
        result_seq.append(
            ApiTailAddressPart(
                name=part.part_value,
                type=part.part_type.name,
            ),
        )
    
    return result_seq