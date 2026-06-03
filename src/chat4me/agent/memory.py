from __future__ import annotations


class ConversationMemory:
    """In-memory conversation history with a maximum message limit."""

    def __init__(self, max_messages: int = 50) -> None:
        self._messages: list[dict[str, str]] = []
        self._max_messages = max_messages

    @property
    def messages(self) -> list[dict[str, str]]:
        """Return a copy of all stored messages."""
        return list(self._messages)

    @property
    def is_empty(self) -> bool:
        """Return True when no messages have been stored."""
        return len(self._messages) == 0

    def add_user_message(self, content: str) -> None:
        """Append a user message and trim if over the limit."""
        self._messages.append({"role": "user", "content": content})
        self._trim()

    def add_assistant_message(self, content: str) -> None:
        """Append an assistant message and trim if over the limit."""
        self._messages.append({"role": "assistant", "content": content})
        self._trim()

    def clear(self) -> None:
        """Remove all stored messages."""
        self._messages.clear()

    def _trim(self) -> None:
        while len(self._messages) > self._max_messages:
            self._messages.pop(0)

    def last_user_message(self) -> str | None:
        """Return the most recent user message, or None."""
        for msg in reversed(self._messages):
            if msg["role"] == "user":
                return msg["content"]
        return None

    def last_assistant_message(self) -> str | None:
        """Return the most recent assistant message, or None."""
        for msg in reversed(self._messages):
            if msg["role"] == "assistant":
                return msg["content"]
        return None

    def __len__(self) -> int:
        return len(self._messages)
