import json
import re


def parse_tool_call(reply: str):
    """
    Parse JSON tool calls.

    Supports:

    {
        ...
    }

    and

    ```json
    {
        ...
    }
    ```
    """

    reply = reply.strip()

    # Remove markdown code fences if present
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", reply, re.DOTALL)

    if match:
        reply = match.group(1).strip()

    try:
        tool = json.loads(reply)

        if isinstance(tool, dict) and "tool" in tool:
            return tool

    except Exception:
        pass

    return None