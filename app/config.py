from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "accounts"

    # PostgreSQL
    postgres_uri: str = "postgresql+asyncpg://user:password@localhost:5432/financedb"
    postgres_pool_size: int = 10
    postgres_max_overflow: int = 20

    # External API
    exchange_rate_api_base: str = "https://api.exchangerate.host"
    exchange_rate_api_key: str = ""

    # App
    app_env: str = "development"
    app_secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


settings = Settings()
