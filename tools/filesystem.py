from pathlib import Path
from config import WORKSPACE_DIR


def _safe_path(path: str) -> Path:
    """
    Resolve a path and ensure it's within WORKSPACE_DIR.
    Returns the resolved Path or raises ValueError.
    """
    workspace = Path(WORKSPACE_DIR).resolve()
    resolved = (workspace / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()

    # Check if resolved path is within workspace
    if not str(resolved).startswith(str(workspace)):
        raise ValueError(f"Access denied: path '{path}' is outside workspace directory.")

    return resolved


def read_file(path: str):
    """Read a file (must be within workspace)."""
    try:
        safe = _safe_path(path)
        return {
            "success": True,
            "content": safe.read_text(encoding="utf-8")
        }
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def write_file(path: str, content: str):
    """Create or overwrite a file (must be within workspace)."""
    try:
        safe = _safe_path(path)
        safe.parent.mkdir(parents=True, exist_ok=True)
        safe.write_text(content, encoding="utf-8")
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_file(path: str):
    """Delete a file (must be within workspace)."""
    try:
        safe = _safe_path(path)
        safe.unlink()
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_directory(path="."):
    """List directory contents (must be within workspace)."""
    try:
        safe = _safe_path(path)
        items = [str(item.name) for item in safe.iterdir()]
        return {"success": True, "items": items}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def exists(path: str):
    """Check if a file exists (must be within workspace)."""
    try:
        safe = _safe_path(path)
        return {"success": True, "exists": safe.exists()}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}
