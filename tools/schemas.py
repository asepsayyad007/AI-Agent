"""
JSON schemas and validation for tool call inputs.
Ensures all tool arguments are valid before execution.
"""


# Tool schemas: defines required fields and their types for each tool
SCHEMAS = {
    # Terminal
    "terminal": {
        "required": ["command"],
        "properties": {
            "command": {"type": "string"},
            "cwd": {"type": "string"},
        },
    },
    # Filesystem
    "read_file": {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"},
        },
    },
    "write_file": {
        "required": ["path", "content"],
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"},
        },
    },
    "delete_file": {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"},
        },
    },
    "list_directory": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
        },
    },
    "exists": {
        "required": ["path"],
        "properties": {
            "path": {"type": "string"},
        },
    },
    # Git
    "git_status": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
        },
    },
    "git_log": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
            "count": {"type": "integer"},
        },
    },
    "git_diff": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
            "staged": {"type": "boolean"},
        },
    },
    "git_add": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
            "files": {"type": "list"},
        },
    },
    "git_commit": {
        "required": ["message"],
        "properties": {
            "path": {"type": "string"},
            "message": {"type": "string"},
        },
    },
    "git_branch": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
            "name": {"type": "string"},
            "checkout": {"type": "boolean"},
        },
    },
    "git_checkout": {
        "required": ["branch"],
        "properties": {
            "path": {"type": "string"},
            "branch": {"type": "string"},
        },
    },
    "git_push": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
            "remote": {"type": "string"},
            "branch": {"type": "string"},
        },
    },
    "git_pull": {
        "required": [],
        "properties": {
            "path": {"type": "string"},
            "remote": {"type": "string"},
            "branch": {"type": "string"},
        },
    },
    # Browser
    "browse": {
        "required": ["url"],
        "properties": {
            "url": {"type": "string"},
            "action": {"type": "string"},
            "selector": {"type": "string"},
        },
    },
    "search": {
        "required": ["query"],
        "properties": {
            "query": {"type": "string"},
        },
    },
}


def _coerce_type(value, expected_type: str):
    """
    Attempt to coerce a value to the expected type.
    Handles common LLM mistakes like "true" -> True, "3" -> 3.
    """
    if expected_type == "string":
        return str(value)

    if expected_type == "integer":
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    if expected_type == "boolean":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() in ("true", "1", "yes"):
                return True
            if value.lower() in ("false", "0", "no"):
                return False
        return None

    if expected_type == "list":
        if isinstance(value, list):
            return value
        return None

    return value


def validate_tool_call(tool_call: dict) -> dict:
    """
    Validate a tool call against its schema.

    Args:
        tool_call: Dict with 'tool' key and tool-specific arguments.

    Returns:
        Dict with:
          - 'valid': bool
          - 'error': str (if invalid)
          - 'coerced': dict (tool_call with type-coerced values, if valid)
    """
    tool_name = tool_call.get("tool")

    if not tool_name:
        return {"valid": False, "error": "Missing 'tool' field in tool call."}

    if tool_name not in SCHEMAS:
        return {"valid": False, "error": f"Unknown tool: '{tool_name}'."}

    schema = SCHEMAS[tool_name]
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    # Check required fields
    for field in required:
        if field not in tool_call:
            return {
                "valid": False,
                "error": f"Missing required field '{field}' for tool '{tool_name}'.",
            }

    # Type-check and coerce provided fields
    coerced = {"tool": tool_name}
    for field, spec in properties.items():
        if field in tool_call:
            value = tool_call[field]
            expected_type = spec.get("type", "string")
            coerced_value = _coerce_type(value, expected_type)
            if coerced_value is None and value is not None:
                return {
                    "valid": False,
                    "error": f"Field '{field}' for tool '{tool_name}' must be {expected_type}, got {type(value).__name__}.",
                }
            coerced[field] = coerced_value if coerced_value is not None else value

    return {"valid": True, "coerced": coerced}
