# Chat4Me

A local-first AI agent that watches a Discord window, reads new messages, and responds autonomously — with the ability to be kind, sound human, and switch channels as needed.

## How it works

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│  Screen      │────▶│  Vision      │────▶│  LLM      │
│  Capture     │     │  Engine      │     │  Client   │
└─────────────┘     └──────────────┘     └─────┬─────┘
                                                │
┌─────────────┐     ┌──────────────┐           │
│  Automation  │◀────│  Agent       │◀──────────┘
│  (mouse/kbd) │     │  Orchestrator│
└─────────────┘     └──────────────┘
```

1. **Screen Capture** — Uses `mss` to capture the Discord window
2. **Vision Engine** — Uses `pytesseract` OCR to extract text from the screenshot
3. **LLM Client** — Sends new messages to an LLM (Ollama, OpenAI, or Anthropic)
4. **Agent Orchestrator** — Runs the loop: capture → analyze → decide → reply
5. **Automation** — Types and sends replies via `pyautogui` + `pynput`

## Requirements

- Python 3.13+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (for text extraction)
- An LLM backend (Ollama local, or OpenAI/Anthropic API key)

### Ollama setup

```bash
ollama pull llama3.2
ollama serve
```

## Installation

```bash
# Install with uv
uv sync
uv sync --extra dev

# Or with pip
pip install -e .
pip install -e ".[dev]"
```

Install Tesseract OCR:
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) or `winget install --id UB-Mannheim.TesseractOCR`
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

## Usage

```bash
# Show available windows
chat4me --list-windows

# Run with default config (targets "Discord" window, Ollama backend)
chat4me

# Run with a custom config file
chat4me -c config/config.yaml

# Override settings via CLI
chat4me --target-window "DiscordCanary" --llm-backend openai --poll-interval 3.0 --log-level DEBUG

# Use a specific config + overrides
chat4me -c myconfig.yaml --llm-backend anthropic
```

## Configuration

Copy `config/config.yaml` to `config.local.yaml` and modify as needed:

| Setting | Default | Description |
|---------|---------|-------------|
| `app.poll_interval` | `2.0` | Seconds between screen captures |
| `app.cooldown_after_reply` | `5.0` | Seconds to wait after sending a message |
| `app.max_consecutive_replies` | `3` | Max replies before forced cooldown |
| `app.target_window` | `"Discord"` | Window title substring to monitor |
| `vision.ocr_lang` | `"eng"` | Tesseract language |
| `vision.tesseract_cmd` | `null` | Custom tesseract path (auto-detect if null) |
| `llm.backend` | `"ollama"` | `ollama`, `openai`, or `anthropic` |
| `llm.ollama.base_url` | `http://localhost:11434` | Ollama server URL |
| `llm.ollama.model` | `llama3.2` | Ollama model name |
| `logging.level` | `"INFO"` | Log level: DEBUG, INFO, WARNING, ERROR |

All config values can be overridden with environment variables using the `CHAT4ME_` prefix (e.g., `CHAT4ME_APP_POLL_INTERVAL=3.0`).

## Project Structure

```
src/chat4me/
├── __init__.py          # Package entry point
├── main.py              # CLI with argparse
├── config.py            # Pydantic config (YAML + env + defaults)
├── agent/
│   ├── memory.py        # Conversation history
│   └── orchestrator.py  # Main agent loop
├── automation/
│   ├── mouse.py         # Mouse control (pyautogui + pynput)
│   └── keyboard.py      # Keyboard control (pyautogui + pynput)
├── llm/
│   ├── client.py        # Ollama / OpenAI / Anthropic clients
│   └── prompts.py       # Prompt builder
├── screen/
│   ├── capture.py       # Screenshot via mss
│   └── window.py        # Window detection via pygetwindow
├── utils/
│   └── logging.py       # Loguru setup
└── vision/
    ├── ocr.py           # Tesseract wrapper
    └── analyzer.py      # Screen state analysis
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov

# Run specific test module
pytest tests/test_agent/
```

84 tests across all modules (config, screen, vision, LLM, automation, agent, CLI).

## License

MIT
