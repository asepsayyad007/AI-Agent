import subprocess
from config import BLOCKED_COMMANDS


def is_blocked(command: str) -> bool:
    """Check if a command matches the blocklist."""
    cmd_lower = command.lower().strip()
    for blocked in BLOCKED_COMMANDS:
        if blocked.lower() in cmd_lower:
            return True
    return False


def run(command: str):
    """
    Execute a shell command with safety checks.
    Returns stdout, stderr, and return code.
    """

    # Check against blocklist
    if is_blocked(command):
        return {
            "stdout": "",
            "stderr": f"BLOCKED: Command rejected by security policy.",
            "returncode": -1,
        }

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "ERROR: Command timed out after 60 seconds.",
            "returncode": -1,
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"ERROR: {str(e)}",
            "returncode": -1,
        }
