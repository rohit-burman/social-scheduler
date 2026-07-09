from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "social_schedular"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "replace-me"
    access_token_expire_minutes:int=15


settings = Settings()
