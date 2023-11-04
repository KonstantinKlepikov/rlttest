from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):

    MONGODB_URL: SecretStr
    DB_NAME: str
    TG_API_TOKEN: SecretStr


settings = Settings()
