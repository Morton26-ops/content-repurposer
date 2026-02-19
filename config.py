from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    model: str = "claude-opus-4-6"
    max_tokens: int = 4096
    max_content_chars: int = 80_000

    model_config = {"env_file": ".env"}


settings = Settings()
