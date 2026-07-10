"""
Token and context management for the AI Agent.
Provides token estimation, counting, and auto-truncation of conversation history.
"""

from config import MAX_CONTEXT_TOKENS


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a string.
    Uses a heuristic: max(chars/4, words*1.3)
    This approximates tokenizer behavior without requiring tiktoken.
    """
    if not text:
        return 0

    char_estimate = len(text) // 4
    word_estimate = int(len(text.split()) * 1.3)

    return max(char_estimate, word_estimate)


def count_message_tokens(messages: list) -> int:
    """
    Count total estimated tokens across all messages.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.

    Returns:
        Total estimated token count.
    """
    total = 0
    for msg in messages:
        content = msg.get("content", "")
        # Add overhead for role/formatting (~4 tokens per message)
        total += estimate_tokens(content) + 4
    return total


def get_token_usage(messages: list) -> dict:
    """
    Get current token usage statistics.

    Args:
        messages: Current conversation history.

    Returns:
        Dict with 'used', 'max', and 'percentage' keys.
    """
    used = count_message_tokens(messages)
    max_tokens = MAX_CONTEXT_TOKENS
    percentage = round((used / max_tokens) * 100, 1) if max_tokens > 0 else 0

    return {
        "used": used,
        "max": max_tokens,
        "percentage": percentage,
    }


def truncate_history(messages: list, preserve_last: int = 4) -> list:
    """
    Truncate conversation history when it exceeds MAX_CONTEXT_TOKENS.
    Preserves the most recent messages.

    Args:
        messages: Full conversation history.
        preserve_last: Number of recent messages to always keep.

    Returns:
        Truncated message list that fits within token budget.
    """
    if not messages:
        return messages

    current_tokens = count_message_tokens(messages)

    if current_tokens <= MAX_CONTEXT_TOKENS:
        return messages

    # Always preserve the last N messages
    preserved = messages[-preserve_last:] if len(messages) > preserve_last else messages[:]

    # If preserved messages alone exceed budget, return them anyway
    # (we can't truncate below the minimum)
    if count_message_tokens(preserved) >= MAX_CONTEXT_TOKENS:
        return preserved

    # Try to include older messages from the front until budget is reached
    remaining_budget = MAX_CONTEXT_TOKENS - count_message_tokens(preserved)
    older_messages = messages[:-preserve_last] if len(messages) > preserve_last else []

    included = []
    for msg in reversed(older_messages):
        msg_tokens = estimate_tokens(msg.get("content", "")) + 4
        if remaining_budget - msg_tokens >= 0:
            included.insert(0, msg)
            remaining_budget -= msg_tokens
        else:
            break

    return included + preserved
