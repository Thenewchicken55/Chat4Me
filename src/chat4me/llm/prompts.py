SYSTEM_PROMPT = (
    "You are a friendly, kind person chatting in a Discord server. "
    "Be natural, concise, and human-like. Use casual language. "
    "If someone asks you something, answer helpfully. "
    "Don't reveal that you are an AI bot. "
    "To switch to a different channel, start your response with "
    "[switch:#channel-name] followed by your message."
)


def build_chat_prompt(
    conversation_history: list[dict[str, str]],
    new_messages: list[str],
    system_prompt: str | None = None,
) -> list[dict[str, str]]:
    """Build a message list for the LLM from conversation history and new messages."""
    messages = [{"role": "system", "content": system_prompt or SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    for msg in new_messages:
        messages.append({"role": "user", "content": msg})
    return messages


def parse_response(response: str) -> str:
    """Strip whitespace from the raw LLM response."""
    return response.strip()


def parse_action(response: str) -> tuple[str | None, str]:
    """Parse a response for a [switch:#channel] action prefix.

    Returns (channel_name, remaining_message) or (None, full_response).
    """
    stripped = response.strip()
    if stripped.startswith("[switch:") and "]" in stripped:
        end_bracket = stripped.index("]")
        channel = stripped[len("[switch:"):end_bracket].strip()
        remainder = stripped[end_bracket + 1:].strip()
        return channel, remainder
    return None, stripped
