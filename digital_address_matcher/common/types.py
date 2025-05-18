"""Основные типы."""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass

class EntityPriorities(Enum):

    Region = 1
    District = 2
    Settlement = 3
    Street = 5
    ZipCode = 6
    House = 7
    Building = 8
    Apartment = 9
    

class LevelEnum(Enum):
    
    FIRST: int = 1
    SECOND: int = 2
    THIRD: int = 3
    FOURTH: int = 4
    FIFTH: int = 5
    
@dataclass
class CodeWithLevel:

    code: List[str]
    level: int
    
@dataclass
class NormalizedKladrHierarchy:
    """Иерархия КЛАДР в нормализованном виде. Нужен в основном для оценки - например, для построения F1 по увроням."""

    level_1: Optional[CodeWithLevel] = None
    level_2: Optional[CodeWithLevel] = None
    level_3: Optional[CodeWithLevel] = None
    level_4: Optional[CodeWithLevel] = None
    level_5: Optional[CodeWithLevel] = None
    
    
    
    
class ModelEnum(Enum):
    """Энам для выбора модели."""
    
    BERT_NER_CASE: int = 1
    NATASHA_CASE: int = 2

class InputAddressPart:
    
    def __init__(self, part_type: EntityPriorities, part_value: str):
        self.part_type: EntityPriorities = part_type
        self.part_value: str = part_value
        

class OutputAddressPart:
    
    def __init__(self, code: str, parent_code: str, name: str, socr: str, level: int, *args):
        self.code: str = code
        self.parent_code: str = parent_code
        self.name: str = name
        self.socr: str = socr
        self.level: int = level