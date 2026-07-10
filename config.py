import ollama

# ==========================================
# MODEL CONFIGURATION
# ==========================================

# Default model for general tasks
MODEL = "qwen2.5-coder:7b"

# Model presets for different task types
MODELS = {
    "default": "qwen2.5-coder:7b",
    "fast": "qwen2.5-coder:3b",
    "heavy": "qwen2.5-coder:14b",
    "reason": "deepseek-r1:8b",
}

# Active model (can be changed at runtime)
_active_model = MODEL


def get_model():
    """Get the currently active model."""
    return _active_model


def set_model(name_or_preset: str):
    """
    Switch the active model.

    Args:
        name_or_preset: Either a preset name (fast, heavy, reason)
                       or a full model name (e.g. 'llama3:8b')
    """
    global _active_model

    if name_or_preset in MODELS:
        _active_model = MODELS[name_or_preset]
    else:
        _active_model = name_or_preset

    return _active_model


def list_models():
    """List all available models from Ollama."""
    try:
        models = ollama.list()
        return {
            "success": True,
            "models": [m["name"] for m in models["models"]],
            "active": _active_model,
            "presets": MODELS,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
