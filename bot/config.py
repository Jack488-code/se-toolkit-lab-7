"""Configuration loader for the bot."""

from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """Bot configuration loaded from environment variables."""

    bot_token: str = ""
    lms_api_url: str = "http://localhost:42002"
    lms_api_key: str = "my-secret-api-key"
    llm_api_key: str = ""
    llm_api_base_url: str = "http://localhost:42005/v1"
    llm_api_model: str = "coder-model"

    class Config:
        env_file = ".env.bot.secret"
        env_file_encoding = "utf-8"


def load_config() -> BotConfig:
    """Load configuration from environment or .env file."""
    return BotConfig()
