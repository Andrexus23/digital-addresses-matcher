"""Модуль API роутеров."""
from fastapi import APIRouter
from digital_address_matcher.routers._tags import TAG_NAME_MATCHER, TAG_NAME_DB_PREPROCESSING
from digital_address_matcher.routers.matcher import match_router
from digital_address_matcher.routers.prepare_kladr import prepare_db_router


root_router = APIRouter()
root_router.include_router(match_router)
root_router.include_router(prepare_db_router)

tags_meta = [
    {
        'name': TAG_NAME_MATCHER,
        'description': 'Матчер',
    },
    {
        'name': TAG_NAME_DB_PREPROCESSING,
        'description': 'Предобработка базы данных КЛАДР',
    },
]