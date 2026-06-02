from chat4me.agent.memory import ConversationMemory


def test_empty_memory():
    mem = ConversationMemory()
    assert mem.is_empty
    assert len(mem) == 0
    assert mem.messages == []
    assert mem.last_user_message() is None
    assert mem.last_assistant_message() is None


def test_add_user_message():
    mem = ConversationMemory()
    mem.add_user_message("Hello")
    assert not mem.is_empty
    assert len(mem) == 1
    assert mem.messages[0] == {"role": "user", "content": "Hello"}
    assert mem.last_user_message() == "Hello"


def test_add_assistant_message():
    mem = ConversationMemory()
    mem.add_assistant_message("Hi there!")
    assert len(mem) == 1
    assert mem.messages[0] == {"role": "assistant", "content": "Hi there!"}
    assert mem.last_assistant_message() == "Hi there!"


def test_conversation_order():
    mem = ConversationMemory()
    mem.add_user_message("Hello")
    mem.add_assistant_message("Hi!")
    mem.add_user_message("How are you?")
    assert len(mem) == 3
    assert [m["role"] for m in mem.messages] == ["user", "assistant", "user"]
    assert mem.last_user_message() == "How are you?"
    assert mem.last_assistant_message() == "Hi!"


def test_clear():
    mem = ConversationMemory()
    mem.add_user_message("Hello")
    mem.add_assistant_message("Hi")
    mem.clear()
    assert mem.is_empty
    assert len(mem) == 0


def test_max_messages():
    mem = ConversationMemory(max_messages=3)
    mem.add_user_message("1")
    mem.add_assistant_message("A")
    mem.add_user_message("2")
    mem.add_user_message("3")
    assert len(mem) == 3
    assert mem.messages[0]["content"] == "A"
    assert mem.messages[-1]["content"] == "3"


def test_last_user_message_empty():
    mem = ConversationMemory()
    mem.add_assistant_message("Hello")
    assert mem.last_user_message() is None


def test_last_assistant_message_empty():
    mem = ConversationMemory()
    assert mem.last_assistant_message() is None
