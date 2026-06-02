from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class OllamaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_OLLAMA_")
    base_url: str = "http://localhost:11434"
    model: str = "llama3.2-vision"


class OpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_OPENAI_")
    api_key: str = ""
    model: str = "gpt-4o"


class AnthropicConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_ANTHROPIC_")
    api_key: str = ""
    model: str = "claude-3-5-sonnet-20241022"


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_")
    backend: Literal["ollama", "openai", "anthropic"] = "ollama"
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    system_prompt: str = (
        "You are a friendly, kind person chatting in a Discord server. "
        "Be natural, concise, and human-like. Use casual language. "
        "If someone asks you something, answer helpfully. "
        "Don't reveal that you are an AI bot."
    )


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_APP_")
    poll_interval: float = 2.0
    cooldown_after_reply: float = 5.0
    max_consecutive_replies: int = 3
    target_window: str = "Discord"


class ScreenConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_SCREEN_")
    capture_region: list[int] | None = None
    scale_factor: float = 1.0


class VisionConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_VISION_")
    ocr_lang: str = "eng"
    tesseract_cmd: str | None = None


class LoggingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LOGGING_")
    level: str = "INFO"
    file: str = "chat4me.log"


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT4ME_")
    app: AppConfig = Field(default_factory=AppConfig)
    screen: ScreenConfig = Field(default_factory=ScreenConfig)
    vision: VisionConfig = Field(default_factory=VisionConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        path = Path(path)
        if not path.exists():
            return cls()
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data:
            return cls()
        return cls(**data)

    @classmethod
    def load(cls, yaml_path: str | Path | None = None) -> "Config":
        cfg = cls.from_yaml(yaml_path) if yaml_path else cls()
        return cfg
