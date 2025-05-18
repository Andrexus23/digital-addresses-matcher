from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from digital_address_matcher.db.models import Addresses

class AddressService:
    
    def __init__(self, session: Session):
        self.session: Session = session
    
    def get_addresses_where(self, limit=None, offset=None, *args) -> List[Addresses]:
        return self.session.scalars(
            select(Addresses).filter(*args).limit(limit).offset(offset),
        ).all()