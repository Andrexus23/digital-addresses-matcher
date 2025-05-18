import pandas as pd
from typing import Optional, List
from sqlalchemy import text, Engine

class DbImportManager:
    """Менеджер импорта таблиц из csv."""
    
    def __init__(self, engine: Engine):
        self._engine: Engine = engine
    
    def import_table_as_csv(self, table_name: str, primary_key_field: str, primary_key_from_index: bool = True, csv_file: Optional[str] = None, df: Optional[pd.DataFrame] = None):
        if (not csv_file and df is None) or (csv_file and df is not None):
            raise ValueError('You must provide either csv-file path or existing dataframe')
        if csv_file:
            df: pd.DataFrame = pd.read_csv(csv_file)

        if primary_key_from_index:
            df[primary_key_field] = df.index + 1
            
        df.to_sql(
            name=table_name, 
            con=self._engine, 
            index=False, 
            if_exists='replace',
        )
        
        with self._engine.connect() as conn:
            conn.execute(text("ALTER TABLE {0} ADD  PRIMARY KEY ({1});".format(table_name, primary_key_field)))
            conn.commit()
            
    def add_foreign_key(
        self,
        table_name: str,
        foreign_key_field: str,
        foreign_key_field_type: str,
        parent_table_name: str,
        parent_table_primary_key: str,
    ):
        with self._engine.connect() as conn:
            # вставить в середину если ключа нет: ALTER TABLE {table_name} ADD {foreign_key_field} {foreign_key_field_type};
            conn.execute(
                text(
                    f"""
                    ALTER TABLE {table_name} ADD CONSTRAINT fk_{foreign_key_field} FOREIGN KEY({parent_table_primary_key}) REFERENCES {table_name}({parent_table_primary_key});
                    ALTER TABLE {table_name} ADD FOREIGN KEY ({foreign_key_field}) REFERENCES {parent_table_name}({parent_table_primary_key}) ON DELETE SET NULL;
                    """
                )
            )
            conn.commit()
            
    def add_index(
        self,
        index_name: str,
        table_name: str,
        fields: List[str],
    ):
        with self._engine.connect() as conn:
            conn.execute(
                text(
                    f"""
                    CREATE INDEX {index_name} ON {table_name}({''.join([f'{index}, ' for index in fields])[:-2]});
                    """
                )
            )
            conn.commit()
