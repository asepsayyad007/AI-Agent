from pathlib import Path
from config import WORKSPACE


def validate_path(path: str):
    """
    Ensures every filesystem operation stays
    inside the configured workspace.
    """

    target = (WORKSPACE / path).resolve()

    workspace = WORKSPACE.resolve()

    try:
        target.relative_to(workspace)
        return True, target

    except ValueError:

        return False, target