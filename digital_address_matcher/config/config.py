from pydantic_settings import BaseSettings, JsonConfigSettingsSource
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    JsonConfigSettingsSource,
)

class DatabaseSettings(BaseModel):
    """Набор настроек для взаимодействия с БД."""

    database: PostgresDsn

class ApiSettings(BaseModel):
    """Настройки FastAPI."""

    host: str
    port: int



class Settings(BaseSettings):

    api_settings: ApiSettings
    database_settings: DatabaseSettings
    model_config = SettingsConfigDict(json_file='config.json')
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """"""
        return (JsonConfigSettingsSource(settings_cls),)


def get_config() -> Settings:
    """Выгрузка конфиг-файла."""
    return Settings()
    
    
    
    