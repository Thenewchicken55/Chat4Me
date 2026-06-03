# Chat4Me — Implementation Plan

## Overview
A local-first AI agent that watches a Discord window, reads new messages, and responds autonomously — with the ability to switch channels, be kind, and sound human.

## Tech Stack
| Layer | Choice |
|-------|--------|
| Language | Python 3.13 |
| Package manager | `uv` |
| Testing | `pytest` + `pytest-mock` + `pytest-asyncio` |
| Config | `pydantic-settings` + YAML |
| Logging | `loguru` |
| Screen capture | `mss` (fast, cross-platform) |
| Image processing | `opencv-python-headless` |
| OCR | `pytesseract` |
| Desktop automation | `pyautogui` + `pynput` |
| LLM client | `httpx` (for Ollama / OpenAI / Anthropic APIs) |
| Code quality | `ruff` (lint + format) |

## Architecture

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

## Tasks (in order)

### Phase 1 — Project skeleton
- [x] 1.1 `uv init` — create pyproject.toml
- [x] 1.2 Write `.gitignore`
- [x] 1.3 Set up `src/chat4me/` package layout
- [x] 1.4 Set up `tests/` layout
- [x] 1.5 Add project metadata to pyproject.toml (dependencies, tool configs)
- [x] 1.6 Create `config/` directory with sample config YAML
- [x] 1.7 Run `uv sync` to install deps
- [x] 1.8 Verify `pytest` runs (empty test suite passes)
- [x] 1.9 Initial commit

### Phase 2 — Configuration module
- [x] 2.1 Write `src/chat4me/config.py` with pydantic models
- [x] 2.2 Support loading from YAML + env vars + defaults
- [x] 2.3 Write tests for config loading
- [x] 2.4 Update sample config with all fields
- [x] 2.5 Commit

### Phase 3 — Logging & utilities
- [x] 3.1 Write `src/chat4me/utils/__init__.py`
- [x] 3.2 Write `src/chat4me/utils/logging.py` (loguru setup)
- [x] 3.3 Write tests
- [x] 3.4 Commit

### Phase 4 — Screen capture module
- [x] 4.1 Write `src/chat4me/screen/capture.py` (screenshot via mss)
- [x] 4.2 Write `src/chat4me/screen/window.py` (find Discord window)
- [x] 4.3 Write tests with fixtures (saved screenshots)
- [x] 4.4 Commit

### Phase 5 — Vision engine (OCR + analysis)
- [x] 5.1 Write `src/chat4me/vision/ocr.py` (tesseract wrapper)
- [x] 5.2 Write `src/chat4me/vision/analyzer.py` (extract messages, channels, UI state)
- [x] 5.3 Write tests with sample screen fixtures
- [x] 5.4 Commit

### Phase 6 — LLM client
- [x] 6.1 Write `src/chat4me/llm/client.py` (Ollama + OpenAI + Anthropic backends)
- [x] 6.2 Write `src/chat4me/llm/prompts.py` (system prompt, response parser)
- [x] 6.3 Write tests with mock HTTP responses
- [x] 6.4 Commit

### Phase 7 — Desktop automation
- [x] 7.1 Write `src/chat4me/automation/mouse.py` (click, move)
- [x] 7.2 Write `src/chat4me/automation/keyboard.py` (type, send)
- [x] 7.3 Write integration-level tests (mocked)
- [x] 7.4 Commit

### Phase 8 — Agent orchestrator
- [x] 8.1 Write `src/chat4me/agent/memory.py` (conversation history)
- [x] 8.2 Write `src/chat4me/agent/orchestrator.py` (main loop)
- [x] 8.3 Wire up: capture → analyze → LLM → act
- [x] 8.4 Handle channel switching logic
- [x] 8.5 Rate limiting / cooldown
- [x] 8.6 Write tests with all dependencies mocked
- [x] 8.7 Commit

### Phase 9 — CLI entry point
- [x] 9.1 Write `src/chat4me/main.py` with `typer` (or argparse)
- [x] 9.2 Add console_scripts entry in pyproject.toml
- [x] 9.3 Write smoke test
- [x] 9.4 Commit

### Phase 10 — Polish & documentation
- [x] 10.1 Update Readme.md with full usage docs
- [x] 10.2 Add docstrings to all public functions
- [x] 10.3 Verify `ruff` passes
- [x] 10.4 Final commit

## Testing strategy
- Pure logic: unit test with real assertions (config, prompts, memory)
- I/O bound: mock httpx, mss, pyautogui, pytesseract
- Fixtures: store sample screenshots in `tests/fixtures/`
- Run: `pytest` (with optional `--cov`)
