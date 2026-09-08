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


    log_name: str = "simple_llm_chatbot"
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    log_file: str = "logs/app.log"
    log_to_console: bool = True
    log_to_file: bool = True


settings = Settings()
