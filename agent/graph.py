from ollama import chat

from config import MODEL
from agent.prompts import SYSTEM_PROMPT


def ask(messages):

    msgs = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    msgs.extend(messages)

    response = chat(
        model=MODEL,
        messages=msgs
    )

    return response["message"]["content"]