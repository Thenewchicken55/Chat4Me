from chat4me.llm.prompts import SYSTEM_PROMPT, build_chat_prompt, parse_response


def test_system_prompt_default():
    assert "friendly" in SYSTEM_PROMPT
    assert "Discord" in SYSTEM_PROMPT


def test_build_chat_prompt_basic():
    history = [{"role": "assistant", "content": "Hey!"}]
    new_msgs = ["What's up?"]
    messages = build_chat_prompt(history, new_msgs)
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Hey!"
    assert messages[2]["role"] == "user"
    assert messages[2]["content"] == "What's up?"


def test_build_chat_prompt_custom_system():
    messages = build_chat_prompt([], ["hello"], system_prompt="Custom prompt")
    assert messages[0]["content"] == "Custom prompt"


def test_build_chat_prompt_no_history():
    messages = build_chat_prompt([], ["first", "second"])
    assert len(messages) == 3
    assert messages[1]["content"] == "first"
    assert messages[2]["content"] == "second"


def test_parse_response():
    assert parse_response("  hello world  ") == "hello world"
    assert parse_response("") == ""
