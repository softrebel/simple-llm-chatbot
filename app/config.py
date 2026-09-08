from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    openai_api_key: str
    openai_base_url: str
    model_name: str = "gpt-4o-mini"

    search_timeout: int = 10
    search_limit: int = 5

    socks_proxy: str | None = None


settings = Settings()
