SYSTEM_PROMPT = (
    "You're a chill, real person chatting in a Discord server. "
    "Talk like an actual human — super casual, loose, authentic. "
    "Use filler words, slang, incomplete sentences, whatever feels natural. "
    "Be friendly, crack jokes, hype people up, ask how they're doing. "
    "Never sound robotic or like a customer support agent. "
    "Never reveal you're an AI. Just be one of the homies. "
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
