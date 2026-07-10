from ollama import chat

from config import get_model
from agent.prompts import SYSTEM_PROMPT


def ask(messages):
    """
    Send conversation to Ollama and return AI response.
    Uses the currently active model from config.
    """

    all_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    all_messages.extend(messages)

    response = chat(
        model=get_model(),
        messages=all_messages
    )

    return response["message"]["content"]
