from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, literal_column
from digital_address_matcher.db.models import Kladr
from typing import List, List
from digital_address_matcher.preprocessing.bert_ner_utils.parse_utils import InputAddressPart, OutputAddressPart




class KladrService:
    
    def __init__(self, session: Session):
        self.session: Session = session
    
    def get_addresses_where(self, **kwargs) -> List[Kladr]:
        return self.session.scalars(
            select(Kladr).filter_by(**kwargs),
        ).all()

    
    def get_kladr_codes_by_addr_parts(self, parts: List[InputAddressPart]) -> List[OutputAddressPart]:
        """Выбрать иерархию КЛАДР."""
        parts_values = [addr.part_value for addr in parts]
        levels = [i for i in range(1, len(parts_values) + 1)]
        
        anchor = select(
            Kladr.code,
            Kladr.parent_code,
            Kladr.name,
            Kladr.socr,
            literal_column('1').label('level')
        ).filter(
            and_(
                Kladr.parent_code.is_(None),
                Kladr.name == parts_values.pop(0),
            )
        )
        hierarchy = anchor.cte('hierarchy', recursive=True)
        
        conditions = []
        for level, part_value in zip(levels, parts_values):
            conditions.append(
                and_(
                    hierarchy.c.level == level,
                    Kladr.name == part_value,
                ),
            )
        conditions = tuple(conditions)
        
        recursive_part = select(
            Kladr.code,
            Kladr.parent_code,
            Kladr.name,
            Kladr.socr,
            (hierarchy.c.level + 1).label('level'),
        ).join(hierarchy, Kladr.parent_code == hierarchy.c.code).where(
            or_(*conditions),
        )
        hierarchy = hierarchy.union_all(recursive_part)
        query = select(hierarchy.c.code, hierarchy.c.parent_code, hierarchy.c.name, hierarchy.c.socr, hierarchy.c.level).select_from(hierarchy)
        result_parts = self.session.execute(query).all()
        return [OutputAddressPart(*part) for part in result_parts]
