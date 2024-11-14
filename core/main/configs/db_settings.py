import urllib.parse
from functools import lru_cache
from os import getenv
from typing import Any, Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator

load_dotenv(find_dotenv('.env'))


class Settings(BaseSettings):
    DB_URL: PostgresDsn = PostgresDsn.build(
        scheme='postgresql+pg8000',
        user=getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'),
        host=getenv('POSTGRES_HOST'),
        path='/' + getenv('POSTGRES_DB'),
    )
    
    # 60 minutes * 8 = 8 hours
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8 

    @validator('DB_URL', pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+pg8000',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


@lru_cache
def get_settings():
    settings = Settings()

    url = settings.DB_URL
    password = urllib.parse.quote_plus(url.password)
    settings.DB_URL = (
        f'{url.scheme}://{url.user}:{password}@{url.host}{url.path}'
    )

    return settings
