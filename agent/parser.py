import json
import re


def parse_ai_response(reply: str):
    """
    Parse AI response into one of:
    - text
    - tool
    - plan
    """

    text = reply.strip()

    # Extract JSON from markdown blocks
    match = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        text,
        re.DOTALL,
    )

    if match:
        text = match.group(1).strip()

    try:
        obj = json.loads(text)

        if isinstance(obj, dict):

            # Planner response
            if "plan" in obj:
                return {
                    "type": "plan",
                    "data": obj,
                }

            # Legacy single tool
            if "tool" in obj:
                return {
                    "type": "tool",
                    "data": obj,
                }

    except Exception:
        pass

    return {
        "type": "text",
        "data": reply,
    }