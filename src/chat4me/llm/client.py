from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import httpx

from chat4me.config import LLMConfig


class LLMClient(ABC):
    """Abstract base for LLM API clients."""

    @abstractmethod
    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Send a message history and return the assistant's reply."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Release any HTTP resources."""
        ...


class OllamaClient(LLMClient):
    """Client for Ollama's local API."""

    def __init__(self, config: LLMConfig) -> None:
        self.base_url = config.ollama.base_url.rstrip("/")
        self.model = config.ollama.model
        self._client = httpx.AsyncClient(timeout=120)

    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Send messages to Ollama's /api/chat endpoint and return the reply."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            **kwargs,
        }
        resp = await self._client.post(f"{self.base_url}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"].strip()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()


class OpenAIClient(LLMClient):
    """Client for the OpenAI Chat Completions API."""

    def __init__(self, config: LLMConfig) -> None:
        self.api_key = config.openai.api_key
        self.model = config.openai.model
        self._client = httpx.AsyncClient(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=120,
        )

    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Send messages to OpenAI and return the assistant's reply."""
        payload = {"model": self.model, "messages": messages, **kwargs}
        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()


class AnthropicClient(LLMClient):
    """Client for the Anthropic Messages API."""

    def __init__(self, config: LLMConfig) -> None:
        self.api_key = config.anthropic.api_key
        self.model = config.anthropic.model
        self._client = httpx.AsyncClient(
            base_url="https://api.anthropic.com/v1",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            timeout=120,
        )

    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Send messages to Anthropic and return the assistant's reply."""
        system_msgs = [m for m in messages if m["role"] == "system"]
        chat_msgs = [m for m in messages if m["role"] != "system"]

        payload: dict[str, Any] = {"model": self.model, "max_tokens": 1024, **kwargs}
        if system_msgs:
            payload["system"] = system_msgs[-1]["content"]
        payload["messages"] = chat_msgs

        resp = await self._client.post("/messages", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"].strip()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()


def create_client(config: LLMConfig) -> LLMClient:
    """Factory — return the appropriate LLMClient subclass based on config.backend."""
    match config.backend:
        case "ollama":
            return OllamaClient(config)
        case "openai":
            return OpenAIClient(config)
        case "anthropic":
            return AnthropicClient(config)
        case _:
            raise ValueError(f"Unknown LLM backend: {config.backend}")
