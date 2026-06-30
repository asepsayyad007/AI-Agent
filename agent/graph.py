from ollama import chat

from config import MODEL
from agent.prompts import SYSTEM_PROMPT


def ask(messages):
    """
    Send conversation to Ollama and return AI response.
    """

    all_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    all_messages.extend(messages)

    response = chat(
        model=MODEL,
        messages=all_messages
    )

    return response["message"]["content"]