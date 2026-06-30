from pathlib import Path


def read_file(path: str):
    """
    Read a file.
    """

    try:
        return {
            "success": True,
            "content": Path(path).read_text(encoding="utf-8")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def write_file(path: str, content: str):
    """
    Create or overwrite a file.
    """

    try:

        file = Path(path)

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
    """
    Delete a file.
    """

    try:

        Path(path).unlink()

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def list_directory(path="."):
    """
    List directory contents.
    """

    try:

        items = []

        for item in Path(path).iterdir():

            items.append(str(item))

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

    return {
        "success": True,
        "exists": Path(path).exists()
    }