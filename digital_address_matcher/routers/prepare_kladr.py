"""Эндпоинты обработки БД."""
from fastapi import APIRouter, HTTPException, status, Query
from digital_address_matcher.routers import TAG_NAME_DB_PREPROCESSING
from digital_address_matcher.db.base import engine
from digital_address_matcher.db.db_import_manager import DbImportManager
from digital_address_matcher.preprocessing.preprocess_kladr_manager import PreprocessKladrManager
from digital_address_matcher.preprocessing.preprocess_address_manager import PreprocessAddressManager
from digital_address_matcher.preprocessing.preprocess_kladr_manager import TYPE_CONFIG_KLADR_BASE, TYPE_CONFIG_KLADR_WITH_PARENT_CODES


prepare_db_router = APIRouter(
    prefix='/preprocess-kladr',
    tags=[TAG_NAME_DB_PREPROCESSING],
)

@prepare_db_router.put(path='/preprocess-kladr-file')
def preprocess_kladr_file(
    source_file: str = Query(description='Путь ко входному файлу в хранилище'),
    destination_file: str = Query(description='Путь к выходному файлу в хранилище'),
):
    """Предобработка файла, содержащего КЛАДР."""
    try:
        kladr_manager = PreprocessKladrManager(
            df_str=source_file, 
            type_config=TYPE_CONFIG_KLADR_BASE,
        )
        kladr_manager.delete_non_actual_codes()
        kladr_manager.find_sequences(parent_field = 'parent_code')
        kladr_manager.save(destination_file)
        return {'message': f'Файл успешно предобработан и сохранён в {destination_file}'}
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Файла {source_file} не существует')
    
    
@prepare_db_router.put(path='/preprocess-addresses-file')
def preprocess_addresses_file(
    source_file: str = Query(description='Путь ко входному файлу в хранилище'),
    destination_file: str = Query(description='Путь к выходному файлу в хранилище'),
):
    """Предобработка файла, содержащего адреса."""
    try:
        address_manager = PreprocessAddressManager(
            df_str=source_file,
        )
        address_manager.save(destination_file)
        return {'message': f'Файл успешно предобработан и сохранён в {destination_file}'}
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Файла {source_file} не существует')
        

@prepare_db_router.put(path='/import-addresses-table-from-file')
def import_addresses_table_from_file(
    source_file: str = Query(description='Путь ко входному файлу в хранилище, из которого будет импорт в БД'),
):
    """Импорт таблицы адресов из подготовленного файла."""
    try:
        address_manager = PreprocessAddressManager(source_file)
        db_import_manager = DbImportManager(engine=engine)
        db_import_manager.import_table_as_csv(df=address_manager.df, table_name='addresses', primary_key_field='addresses_id')
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Файла {source_file} не существует')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@prepare_db_router.put(path='/import-kladr-table-from-file')
def import_kladr_table_from_file(
    source_file: str = Query(description='Путь ко входному файлу в хранилище, из которого будет импорт в БД'),
):
    """Импорт таблицы КЛАДР из подготовленного файла."""
    try:
        kladr_manager = PreprocessKladrManager(df_str=source_file, type_config=TYPE_CONFIG_KLADR_WITH_PARENT_CODES)
        db_import_manager = DbImportManager(engine=engine)
        db_import_manager.import_table_as_csv(df=kladr_manager.df, table_name='kladr', primary_key_field='code', primary_key_from_index=False)
        db_import_manager.add_foreign_key(
            table_name='kladr', foreign_key_field='parent_code', foreign_key_field_type='str', parent_table_name='kladr', parent_table_primary_key='code',
        )
        db_import_manager.add_index('kladr_index', 'kladr', ['name', 'socr', 'code', 'index', 'gninmb', 'uno', 'ocatd', 'status', 'parent_code'])
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Файла {source_file} не существует')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))