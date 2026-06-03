from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OllamaConfig(BaseSettings):
    """Configuration for the Ollama LLM backend."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_OLLAMA_")
    base_url: str = "http://localhost:11434"
    model: str = "llama3.2"


class OpenAIConfig(BaseSettings):
    """Configuration for the OpenAI LLM backend."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_OPENAI_")
    api_key: str = ""
    model: str = "gpt-4o"


class AnthropicConfig(BaseSettings):
    """Configuration for the Anthropic LLM backend."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LLM_ANTHROPIC_")
    api_key: str = ""
    model: str = "claude-3-5-sonnet-20241022"


class LLMConfig(BaseSettings):
    """Configuration for LLM backend selection and credentials."""

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
    """Configuration for application behaviour — polling, cooldowns, target window."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_APP_")
    poll_interval: float = 2.0
    cooldown_after_reply: float = 5.0
    max_consecutive_replies: int = 3
    target_window: str = "Discord"


class ScreenConfig(BaseSettings):
    """Configuration for screen capture behaviour."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_SCREEN_")
    capture_region: list[int] | None = None
    scale_factor: float = 1.0


class VisionConfig(BaseSettings):
    """Configuration for OCR and vision processing."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_VISION_")
    ocr_lang: str = "eng"
    tesseract_cmd: str | None = None


class LoggingConfig(BaseSettings):
    """Configuration for logging level and output file."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_LOGGING_")
    level: str = "INFO"
    file: str = "chat4me.log"


class Config(BaseSettings):
    """Root configuration that composes all sub-configs and supports YAML loading."""

    model_config = SettingsConfigDict(env_prefix="CHAT4ME_")
    app: AppConfig = Field(default_factory=AppConfig)
    screen: ScreenConfig = Field(default_factory=ScreenConfig)
    vision: VisionConfig = Field(default_factory=VisionConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        """Load configuration from a YAML file, merging with defaults."""
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
        """Load config from YAML, env vars, and defaults.

        If *yaml_path* is provided it is used; otherwise
        ``config/config.yaml`` relative to the working directory
        is tried as a fallback.
        """
        if yaml_path:
            return cls.from_yaml(yaml_path)
        default = Path("config/config.yaml")
        if default.exists():
            return cls.from_yaml(default)
        return cls()
