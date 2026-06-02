SYSTEM_PROMPT = (
    "You are a friendly, kind person chatting in a Discord server. "
    "Be natural, concise, and human-like. Use casual language. "
    "If someone asks you something, answer helpfully. "
    "Don't reveal that you are an AI bot."
)


def build_chat_prompt(
    conversation_history: list[dict[str, str]],
    new_messages: list[str],
    system_prompt: str | None = None,
) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": system_prompt or SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    for msg in new_messages:
        messages.append({"role": "user", "content": msg})
    return messages


def parse_response(response: str) -> str:
    return response.strip()
