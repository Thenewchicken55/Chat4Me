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
- [ ] 1.1 `uv init` — create pyproject.toml
- [ ] 1.2 Write `.gitignore`
- [ ] 1.3 Set up `src/chat4me/` package layout
- [ ] 1.4 Set up `tests/` layout
- [ ] 1.5 Add project metadata to pyproject.toml (dependencies, tool configs)
- [ ] 1.6 Create `config/` directory with sample config YAML
- [ ] 1.7 Run `uv sync` to install deps
- [ ] 1.8 Verify `pytest` runs (empty test suite passes)
- [ ] 1.9 Initial commit

### Phase 2 — Configuration module
- [ ] 2.1 Write `src/chat4me/config.py` with pydantic models
- [ ] 2.2 Support loading from YAML + env vars + defaults
- [ ] 2.3 Write tests for config loading
- [ ] 2.4 Update sample config with all fields
- [ ] 2.5 Commit

### Phase 3 — Logging & utilities
- [ ] 3.1 Write `src/chat4me/utils/__init__.py`
- [ ] 3.2 Write `src/chat4me/utils/logging.py` (loguru setup)
- [ ] 3.3 Write tests
- [ ] 3.4 Commit

### Phase 4 — Screen capture module
- [ ] 4.1 Write `src/chat4me/screen/capture.py` (screenshot via mss)
- [ ] 4.2 Write `src/chat4me/screen/window.py` (find Discord window)
- [ ] 4.3 Write tests with fixtures (saved screenshots)
- [ ] 4.4 Commit

### Phase 5 — Vision engine (OCR + analysis)
- [ ] 5.1 Write `src/chat4me/vision/ocr.py` (tesseract wrapper)
- [ ] 5.2 Write `src/chat4me/vision/analyzer.py` (extract messages, channels, UI state)
- [ ] 5.3 Write tests with sample screen fixtures
- [ ] 5.4 Commit

### Phase 6 — LLM client
- [ ] 6.1 Write `src/chat4me/llm/client.py` (Ollama + OpenAI + Anthropic backends)
- [ ] 6.2 Write `src/chat4me/llm/prompts.py` (system prompt, response parser)
- [ ] 6.3 Write tests with mock HTTP responses
- [ ] 6.4 Commit

### Phase 7 — Desktop automation
- [ ] 7.1 Write `src/chat4me/automation/mouse.py` (click, move)
- [ ] 7.2 Write `src/chat4me/automation/keyboard.py` (type, send)
- [ ] 7.3 Write integration-level tests (mocked)
- [ ] 7.4 Commit

### Phase 8 — Agent orchestrator
- [ ] 8.1 Write `src/chat4me/agent/memory.py` (conversation history)
- [ ] 8.2 Write `src/chat4me/agent/orchestrator.py` (main loop)
- [ ] 8.3 Wire up: capture → analyze → LLM → act
- [ ] 8.4 Handle channel switching logic
- [ ] 8.5 Rate limiting / cooldown
- [ ] 8.6 Write tests with all dependencies mocked
- [ ] 8.7 Commit

### Phase 9 — CLI entry point
- [ ] 9.1 Write `src/chat4me/main.py` with `typer` (or argparse)
- [ ] 9.2 Add console_scripts entry in pyproject.toml
- [ ] 9.3 Write smoke test
- [ ] 9.4 Commit

### Phase 10 — Polish & documentation
- [ ] 10.1 Update Readme.md with full usage docs
- [ ] 10.2 Add docstrings to all public functions
- [ ] 10.3 Verify `ruff` passes
- [ ] 10.4 Final commit

## Testing strategy
- Pure logic: unit test with real assertions (config, prompts, memory)
- I/O bound: mock httpx, mss, pyautogui, pytesseract
- Fixtures: store sample screenshots in `tests/fixtures/`
- Run: `pytest` (with optional `--cov`)
