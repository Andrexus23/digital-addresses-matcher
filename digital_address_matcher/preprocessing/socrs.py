from typing import Set, Dict
from natasha.grammars.addr import  (
    RESPUBLIKA_WORDS,
    KRAI_WORDS,
    OBLAST_WORDS,
    AUTO_OKRUG_WORDS,
    
    RAION_WORDS,
    
    GOROD_WORDS,
    DEREVNYA_WORDS,
    SELO_WORDS,
    POSELOK_WORDS,
    
    STREET_WORDS,
    PROEZD_WORDS,
    PROSPEKT_WORDS,
    PEREULOK_WORDS,
    PLOSHAD_WORDS,
    SHOSSE_WORDS,
    NABEREG_WORDS,
    BULVAR_WORDS,
    
    DOM_WORDS,
    KORPUS_WORDS,
    STROENIE_WORDS,
    
    OFIS_WORDS,
    KVARTIRA_WORDS,
    
    INDEX,
    
    AddrPart,
)


class Priority:
    
    FIRST: int = 1
    SECOND: int = 2
    THIRD: int = 3
    FIFTH: int = 5
    SIXTH: int = 6
    SEVENTH: int = 7
    EIGHTH: int = 8
    NINTH: int = 9
    LATEST: int = 1e5
    
    
from typing import Set, List

KLADR_SOCRS_SET: Set = {'АО',
 'Аобл',
 'Респ',
 'а/я',
 'аал',
 'автодорога',
 'аллея',
 'арбан',
 'аул',
 'б-р',
 'берег',
 'вал',
 'взв.',
 'волость',
 'въезд',
 'высел',
 'г',
 'г-к',
 'г.о.',
 'городок',
 'гп',
 'гск',
 'д',
 'д.',
 'днп',
 'дор',
 'дп',
 'ж/д бл-ст',
 'ж/д о.п.',
 'ж/д п.п.',
 'ж/д пл-ка',
 'ж/д рзд',
 'ж/д ст',
 'ж/д_будка',
 'ж/д_казарм',
 'ж/д_оп',
 'ж/д_платф',
 'ж/д_пост',
 'ж/д_рзд',
 'ж/д_ст',
 'ж/р',
 'жилзона',
 'жилрайон',
 'жт',
 'заезд',
 'заимка',
 'зона',
 'казарма',
 'кв-л',
 'км',
 'кольцо',
 'кордон',
 'коса',
 'кп',
 'край',
 'линия',
 'лпх',
 'м',
 'массив',
 'мгстр.',
 'местность',
 'месторожд.',
 'мкр',
 'мост',
 'н/п',
 'наб',
 'нп',
 'нп.',
 'обл',
 'округ',
 'остров',
 'п',
 'п.',
 'п. ж/д ст.',
 'п. ст.',
 'п/о',
 'п/р',
 'п/ст',
 'парк',
 'пгт',
 'пер',
 'переезд',
 'пл',
 'пл-ка',
 'пл.р-н',
 'платф',
 'погост',
 'порт',
 'пос.рзд',
 'пос.рзд.',
 'починок',
 'пр-кт',
 'проезд',
 'промзона',
 'просек',
 'просека',
 'проселок',
 'проулок',
 'р-н',
 'рзд',
 'рп',
 'рп.',
 'ряд',
 'ряды',
 'с',
 'с.',
 'с/а',
 'с/мо',
 'с/о',
 'с/п',
 'с/с',
 'с/т',
 'сад',
 'сзд.',
 'сквер',
 'сл',
 'снт',
 'сп',
 'сп.',
 'спуск',
 'ст',
 'ст-ца',
 'стр',
 'тер',
 'тер. ГСК',
 'тер. ДНО',
 'тер. ДНП',
 'тер. ДНТ',
 'тер. ДПК',
 'тер. ОНО',
 'тер. ОНП',
 'тер. ОНТ',
 'тер. ОПК',
 'тер. ПК',
 'тер. СНО',
 'тер. СНП',
 'тер. СНТ',
 'тер. СПК',
 'тер. ТСЖ',
 'тер. ТСН',
 'тер.СОСН',
 'тер.ф.х.',
 'тракт',
 'туп',
 'у',
 'ул',
 'ус.',
 'уч-к',
 'ф/х',
 'ферма',
 'х',
 'х.',
 'ш'}

KLADR_SOCRS_LIST: List = list(KLADR_SOCRS_SET)
KLADR_SOCRS_STR: str = ' '.join(KLADR_SOCRS_LIST)


def get_types_set_from_rules(*args) -> Set[str]:
    """Получить типы из правил."""
    return {arg.interpretator.normalizer.value for arg in args}


PRIORITY_MAP: Dict[Priority, Set[str]] = {
    Priority.FIRST: get_types_set_from_rules(
        RESPUBLIKA_WORDS,
        KRAI_WORDS,
        OBLAST_WORDS,
        AUTO_OKRUG_WORDS,
    ),
    Priority.SECOND: get_types_set_from_rules(
        RAION_WORDS,
    ),
    Priority.THIRD: get_types_set_from_rules(
        GOROD_WORDS,
        DEREVNYA_WORDS,
        SELO_WORDS,
        POSELOK_WORDS,
    ),
    Priority.FIFTH: get_types_set_from_rules(
        STREET_WORDS,
        PROEZD_WORDS,
        PROSPEKT_WORDS,
        PEREULOK_WORDS,
        PLOSHAD_WORDS,
        SHOSSE_WORDS,
        NABEREG_WORDS,
        BULVAR_WORDS,
    ),
    Priority.SIXTH: {'индекс'},
    Priority.SEVENTH: get_types_set_from_rules(
        DOM_WORDS,
    ),
    Priority.EIGHTH: get_types_set_from_rules(
        KORPUS_WORDS,
        STROENIE_WORDS,
    ),
    Priority.NINTH: get_types_set_from_rules(
        OFIS_WORDS,
        KVARTIRA_WORDS,
    ),
}

FULL_SOCRS_SET: set = KLADR_SOCRS_SET.copy()

for val in PRIORITY_MAP.values():
    FULL_SOCRS_SET.update(val)
    
def get_all_socr_variants(socr: str) -> set:
    """Получить все варианты socr вместе с пробелами/точками для простоты выкидывания в трансформере."""
    new_socrs_set = set()
    new_socrs_set.update(
        {
            socr + ' ',
            ' ' + socr,
        },
    )
    if '.' not in socr:
        new_socrs_set.update(
            {
                socr + '. ',
                ' ' + socr + '.',
            },
        )
    return new_socrs_set
