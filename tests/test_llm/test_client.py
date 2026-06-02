import pytest

from chat4me.config import LLMConfig
from chat4me.llm.client import (
    AnthropicClient,
    OllamaClient,
    OpenAIClient,
    create_client,
)


@pytest.fixture
def config():
    return LLMConfig()


@pytest.fixture
def messages():
    return [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello"},
    ]


class TestOllamaClient:
    @pytest.mark.asyncio
    async def test_chat_success(self, config, messages):
        config.ollama.base_url = "http://test:11434"
        config.ollama.model = "test-model"
        client = OllamaClient(config)
        try:
            assert client.base_url == "http://test:11434"
            assert client.model == "test-model"
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_chat_http_error(self, config, messages):
        config.ollama.base_url = "http://localhost:1"
        client = OllamaClient(config)
        with pytest.raises(Exception):
            await client.chat(messages)
        await client.close()


class TestOpenAIClient:
    @pytest.mark.asyncio
    async def test_init(self, config):
        config.openai.api_key = "sk-test"
        config.openai.model = "gpt-4o"
        client = OpenAIClient(config)
        try:
            assert client.model == "gpt-4o"
            assert client.api_key == "sk-test"
        finally:
            await client.close()


class TestAnthropicClient:
    @pytest.mark.asyncio
    async def test_init(self, config):
        config.anthropic.api_key = "sk-ant-test"
        config.anthropic.model = "claude-3-opus"
        client = AnthropicClient(config)
        try:
            assert client.model == "claude-3-opus"
            assert client.api_key == "sk-ant-test"
        finally:
            await client.close()


class TestCreateClient:
    def test_create_ollama(self, config):
        config.backend = "ollama"
        client = create_client(config)
        assert isinstance(client, OllamaClient)

    def test_create_openai(self, config):
        config.backend = "openai"
        config.openai.api_key = "sk-test"
        client = create_client(config)
        assert isinstance(client, OpenAIClient)

    def test_create_anthropic(self, config):
        config.backend = "anthropic"
        config.anthropic.api_key = "sk-ant-test"
        client = create_client(config)
        assert isinstance(client, AnthropicClient)

    def test_create_unknown(self, config):
        config.backend = "invalid"
        with pytest.raises(ValueError, match="Unknown LLM backend"):
            create_client(config)
