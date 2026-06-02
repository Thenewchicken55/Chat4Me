from pathlib import Path

import yaml

from chat4me.config import Config


def test_default_config_has_sane_values():
    cfg = Config()
    assert cfg.app.poll_interval == 2.0
    assert cfg.app.cooldown_after_reply == 5.0
    assert cfg.app.max_consecutive_replies == 3
    assert cfg.app.target_window == "Discord"
    assert cfg.screen.capture_region is None
    assert cfg.screen.scale_factor == 1.0
    assert cfg.vision.ocr_lang == "eng"
    assert cfg.llm.backend == "ollama"
    assert cfg.llm.ollama.base_url == "http://localhost:11434"
    assert cfg.llm.ollama.model == "llama3.2-vision"
    assert cfg.llm.openai.api_key == ""
    assert cfg.llm.anthropic.api_key == ""
    assert cfg.logging.level == "INFO"
    assert cfg.logging.file == "chat4me.log"


def test_from_yaml_loads_values(tmp_path: Path):
    data = {
        "app": {"poll_interval": 3.0, "target_window": "DiscordCanary"},
        "llm": {
            "backend": "openai",
            "openai": {"api_key": "sk-test", "model": "gpt-4o-mini"},
        },
        "logging": {"level": "DEBUG"},
    }
    p = tmp_path / "config.yaml"
    with open(p, "w") as f:
        yaml.dump(data, f)
    cfg = Config.from_yaml(p)
    assert cfg.app.poll_interval == 3.0
    assert cfg.app.target_window == "DiscordCanary"
    assert cfg.llm.backend == "openai"
    assert cfg.llm.openai.api_key == "sk-test"
    assert cfg.llm.openai.model == "gpt-4o-mini"
    assert cfg.logging.level == "DEBUG"
    assert cfg.llm.ollama.base_url == "http://localhost:11434"


def test_from_yaml_missing_file_returns_defaults(tmp_path: Path):
    p = tmp_path / "nonexistent.yaml"
    cfg = Config.from_yaml(p)
    assert cfg.app.poll_interval == 2.0


def test_from_yaml_partial_file_merges_defaults(tmp_path: Path):
    data = {"app": {"poll_interval": 5.0}}
    p = tmp_path / "partial.yaml"
    with open(p, "w") as f:
        yaml.dump(data, f)
    cfg = Config.from_yaml(p)
    assert cfg.app.poll_interval == 5.0
    assert cfg.app.cooldown_after_reply == 5.0
    assert cfg.logging.level == "INFO"


def test_from_yaml_empty_file_returns_defaults(tmp_path: Path):
    p = tmp_path / "empty.yaml"
    p.touch()
    cfg = Config.from_yaml(p)
    assert cfg.app.poll_interval == 2.0


def test_load_with_yaml_path(tmp_path: Path):
    data = {"app": {"poll_interval": 10.0}}
    p = tmp_path / "cfg.yaml"
    with open(p, "w") as f:
        yaml.dump(data, f)
    cfg = Config.load(yaml_path=str(p))
    assert cfg.app.poll_interval == 10.0


def test_load_without_yaml_path():
    cfg = Config.load()
    assert cfg.app.poll_interval == 2.0
