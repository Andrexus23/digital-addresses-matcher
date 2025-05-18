from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from digital_address_matcher.routers import TAG_NAME_MATCHER
from digital_address_matcher.db.base import get_db
from digital_address_matcher.address_matcher.matcher import AddressMatcher, ModelEnum
from digital_address_matcher.api_models.address_parts import ApiAddressPart, ApiKladrAddressPart, ApiTailAddressPart
from digital_address_matcher.api_models.address_parts import parsed_address_to_api


match_router = APIRouter(
    prefix='/match',
    tags=[TAG_NAME_MATCHER],
)



@match_router.post(path='/bert', response_model=List[ApiAddressPart | ApiKladrAddressPart | ApiTailAddressPart])
def match_address_by_bert(
    address: str,
    session: Session = Depends(get_db),
):
    """Преобразовать адрес в последовательность КЛАДР-кодов при помощи aidarmusin/address-ner-ru (BERT)."""
    matcher = AddressMatcher(session)
    matched_addresses = matcher.match([address], model_case=ModelEnum.BERT_NER_CASE)
    if not matched_addresses or not matched_addresses[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось распознать адрес')
    kladr_part, tail_part = matched_addresses[0]
    return parsed_address_to_api(kladr_part, tail_part)
    

@match_router.post(path='/natasha', response_model=List[ApiAddressPart | ApiKladrAddressPart | ApiTailAddressPart])
def match_address_by_natasha(
    address: str,
    session: Session = Depends(get_db),
):
    """Преобразовать адрес в последовательность КЛАДР-кодов при помощи Natasha."""
    matcher = AddressMatcher(session)
    matched_addresses = matcher.match([address], model_case=ModelEnum.NATASHA_CASE)
    if not matched_addresses or not matched_addresses[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось распознать адрес')
    kladr_part, tail_part = matched_addresses[0]
    return parsed_address_to_api(kladr_part, tail_part)