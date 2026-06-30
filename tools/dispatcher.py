from tools.terminal import run


def execute(tool_call: dict):
    """
    Execute a tool based on AI response.

    Returns a dictionary.
    """

    tool = tool_call.get("tool")

    if tool == "terminal":

        command = tool_call.get("command", "")

        result = run(command)

        return {
            "success": True,
            "tool": "terminal",
            "command": command,
            "result": result
        }

    return {
        "success": False,
        "error": f"Unknown tool: {tool}"
    }