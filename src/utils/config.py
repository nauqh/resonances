from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')

    ID: str
    SECRET: str
    DB_URL: str
    OPENAI_KEY: str


settings = Settings()