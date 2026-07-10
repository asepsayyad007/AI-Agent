import time
from ollama import chat

from config import get_model, MAX_RETRIES
from agent.prompts import SYSTEM_PROMPT


def check_ollama():
    """Check if Ollama is running and accessible."""
    try:
        import ollama
        ollama.list()
        return True
    except Exception:
        return False


def ask(messages, retries=3):
    """
    Send conversation to Ollama and return AI response.
    Includes retry logic with exponential backoff.
    """

    all_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    all_messages.extend(messages)

    for attempt in range(retries):
        try:
            response = chat(
                model=get_model(),
                messages=all_messages
            )
            return response["message"]["content"]

        except ConnectionError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return "[ERROR] Cannot connect to Ollama. Make sure it's running with: ollama serve"

        except Exception as e:
            error_str = str(e).lower()

            # Model not found
            if "not found" in error_str or "does not exist" in error_str:
                model = get_model()
                return f"[ERROR] Model '{model}' not found. Pull it with: ollama pull {model}"

            # Retry on transient errors
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue

            return f"[ERROR] Ollama request failed: {str(e)}"
