import re
import os

# Constant used for redacted values
REDACTION_TEXT = "[REDACTED]"

# Path to the sensitive keys file
SENSITIVE_KEYS_FILE = os.path.join(os.path.dirname(__file__), "sensitive_keys.txt")


def load_sensitive_keys():
    """
    Loads sensitive field names (e.g. password, api_key) from the sensitive_keys.txt file
    and compiles regex patterns for each for quick redaction.
    """
    patterns = []
    if not os.path.exists(SENSITIVE_KEYS_FILE):
        return patterns

    with open(SENSITIVE_KEYS_FILE, "r", encoding="utf-8") as f:
        keys = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for key in keys:
        escaped = re.escape(key)
        # Match patterns like:
        # password=abc123, api_key: abcd-efgh, token - xyz
        # Stop capturing at comma, semicolon, or newline
        pattern = re.compile(rf"(?i)\b({escaped})\b\s*[:=\-]\s*([^,;\n]*)")
        patterns.append(pattern)

    return patterns


# Preload all regex patterns at import time for performance
_PATTERNS = load_sensitive_keys()


def redact(message: str) -> str:
    """
    Replaces sensitive values in a log message with [REDACTED].

    Example:
        Input:  "email=user@example.com, password=12345"
        Output: "email=[REDACTED], password=[REDACTED]"
    """
    if not message or not isinstance(message, str):
        return message

    redacted = message
    for pattern in _PATTERNS:
        redacted = pattern.sub(lambda m: f"{m.group(1)}={REDACTION_TEXT}", redacted)
    return redacted
