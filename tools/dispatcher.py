from tools.terminal import run
from tools.filesystem import (
    read_file,
    write_file,
    delete_file,
    list_directory,
    exists,
)


def execute(tool_call: dict):
    """
    Executes any tool requested by the AI.
    """

    tool = tool_call.get("tool")

    # -----------------------------
    # TERMINAL
    # -----------------------------

    if tool == "terminal":

        command = tool_call.get("command", "")

        result = run(command)

        return {
            "success": True,
            "tool": "terminal",
            "command": command,
            "result": result
        }

    # -----------------------------
    # FILESYSTEM
    # -----------------------------

    if tool == "read_file":

        return read_file(
            tool_call["path"]
        )

    if tool == "write_file":

        return write_file(
            tool_call["path"],
            tool_call["content"]
        )

    if tool == "delete_file":

        return delete_file(
            tool_call["path"]
        )

    if tool == "list_directory":

        path = tool_call.get(
            "path",
            "."
        )

        return list_directory(path)

    if tool == "exists":

        return exists(
            tool_call["path"]
        )

    # -----------------------------
    # UNKNOWN TOOL
    # -----------------------------

    return {
        "success": False,
        "error": f"Unknown tool: {tool}"
    }