from tools.terminal import run
from tools.filesystem import (
    read_file,
    write_file,
    delete_file,
    list_directory,
    exists,
)
from tools.git import (
    git_status,
    git_log,
    git_diff,
    git_add,
    git_commit,
    git_branch,
    git_checkout,
    git_push,
    git_pull,
)
from tools.browser import browse, search


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
    # GIT
    # -----------------------------

    if tool == "git_status":
        path = tool_call.get("path", ".")
        return git_status(path)

    if tool == "git_log":
        path = tool_call.get("path", ".")
        count = tool_call.get("count", 10)
        return git_log(path, count)

    if tool == "git_diff":
        path = tool_call.get("path", ".")
        staged = tool_call.get("staged", False)
        return git_diff(path, staged)

    if tool == "git_add":
        path = tool_call.get("path", ".")
        files = tool_call.get("files", None)
        return git_add(path, files)

    if tool == "git_commit":
        path = tool_call.get("path", ".")
        message = tool_call.get("message", "")
        return git_commit(path, message)

    if tool == "git_branch":
        path = tool_call.get("path", ".")
        name = tool_call.get("name", None)
        checkout = tool_call.get("checkout", False)
        return git_branch(path, name, checkout)

    if tool == "git_checkout":
        path = tool_call.get("path", ".")
        branch = tool_call.get("branch", "")
        return git_checkout(path, branch)

    if tool == "git_push":
        path = tool_call.get("path", ".")
        remote = tool_call.get("remote", "origin")
        branch = tool_call.get("branch", None)
        return git_push(path, remote, branch)

    if tool == "git_pull":
        path = tool_call.get("path", ".")
        remote = tool_call.get("remote", "origin")
        branch = tool_call.get("branch", None)
        return git_pull(path, remote, branch)

    # -----------------------------
    # BROWSER
    # -----------------------------

    if tool == "browse":
        url = tool_call.get("url", "")
        action = tool_call.get("action", "text")
        selector = tool_call.get("selector", None)
        return browse(url, action, selector)

    if tool == "search":
        query = tool_call.get("query", "")
        return search(query)

    # -----------------------------
    # UNKNOWN TOOL
    # -----------------------------

    return {
        "success": False,
        "error": f"Unknown tool: {tool}"
    }
