from pathlib import Path

from tools.security import validate_path


def read_file(path: str):

    allowed, file = validate_path(path)

    if not allowed:
        return {
            "success": False,
            "error": "Access denied. Path is outside the workspace."
        }

    try:
        return {
            "success": True,
            "content": file.read_text(encoding="utf-8")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def write_file(path: str, content: str):

    allowed, file = validate_path(path)

    if not allowed:
        return {
            "success": False,
            "error": "Access denied. Path is outside the workspace."
        }

    try:
        file.parent.mkdir(parents=True, exist_ok=True)

        file.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def delete_file(path: str):

    allowed, file = validate_path(path)

    if not allowed:
        return {
            "success": False,
            "error": "Access denied. Path is outside the workspace."
        }

    try:

        file.unlink()

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def list_directory(path=""):

    allowed, directory = validate_path(path)

    if not allowed:
        return {
            "success": False,
            "error": "Access denied. Path is outside the workspace."
        }

    try:

        items = []

        for item in directory.iterdir():
            items.append(item.name)

        return {
            "success": True,
            "items": items
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def exists(path: str):

    allowed, file = validate_path(path)

    if not allowed:
        return {
            "success": False,
            "error": "Access denied. Path is outside the workspace."
        }

    return {
        "success": True,
        "exists": file.exists()
    }