import json
import re


def parse_ai_response(reply: str):
    """
    Parses AI responses.

    Returns:

    {
        "type": "tool",
        "data": {...}
    }

    or

    {
        "type": "plan",
        "data": [...]
    }

    or

    {
        "type": "text",
        "data": "..."
    }
    """

    reply = reply.strip()

    # Remove markdown
    match = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        reply,
        re.DOTALL
    )

    if match:
        reply = match.group(1).strip()

    try:

        obj = json.loads(reply)

        # -------------------------
        # Single Tool
        # -------------------------

        if isinstance(obj, dict):

            if "tool" in obj:

                return {
                    "type": "tool",
                    "data": obj
                }

            # -------------------------
            # Planner
            # -------------------------

            if "plan" in obj:

                return {
                    "type": "plan",
                    "data": obj["plan"]
                }

    except Exception:
        pass

    return {
        "type": "text",
        "data": reply
    }