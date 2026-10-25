from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    APP_NAME: str = "Sales Agent"
    DEBUG: bool = False
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "user"
    DB_PASSWORD: SecretStr = SecretStr("password")
    DB_NAME: str = "sales_agent"
    DB_SCHEMA: str ="sales_agent"

    GEMINI_API_KEY: SecretStr = SecretStr("")
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    @property
    def DATABASE_URL(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.DB_HOST,
            port=self.DB_PORT,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(), # Because the password is now encrypted
            database=self.DB_NAME
            # query={"options": f"-c search_path={self.DB_SCHEMA}"}
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()