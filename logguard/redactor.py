
import re, os
from typing import Iterable, Pattern, List

BASE_DIR = os.path.dirname(__file__)
SENSITIVE_FILE = os.path.join(BASE_DIR, "sensitive_keys.txt")
REDACTION_TEXT = "[REDACTED]"

_default_patterns = [
    # email
    re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"),
    # simple credit card-ish numbers (13-19 digits)
    re.compile(r"\b\d{13,19}\b"),
    # SSN-like
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    # IBAN-ish (very loose)
    re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b")
]

_sensitive_key_patterns: List[Pattern] = []
_loaded = False

def load_sensitive_keys(path: str = SENSITIVE_FILE):
    global _sensitive_key_patterns, _loaded
    if _loaded:
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            keys = [line.strip() for line in f if line.strip()]
    except Exception:
        keys = []
    patterns = []
    for k in keys:
        # build a forgiving pattern that matches e.g. "password", "user-password", "user.password", "userPassword", "user_password1"
        escaped = re.escape(k)
        # attempt to match as a key in "key: value" or "key=value" contexts, or as standalone token
        p = re.compile(r"(?i)(" + escaped + r")\s*[:=\-]\s*([^,\s;]+)")
        patterns.append(p)
        # also match the key anywhere as a token
        p2 = re.compile(r"(?i)\b" + escaped + r"\b")
        patterns.append(p2)
    _sensitive_key_patterns = patterns + _default_patterns
    _loaded = True

def redact(text: str) -> str:
    """
    Redact sensitive substrings from arbitrary text.
    Strategy:
    - Ensure sensitive key patterns are compiled (lazy load)
    - For key:value patterns, replace the value part with REDACTION_TEXT keeping the key visible
    - For general patterns (emails, cards) replace matches with REDACTION_TEXT
    """
    if not _loaded:
        load_sensitive_keys()
    s = text
    # first handle key:value patterns (keep key, redact value)
    for p in _sensitive_key_patterns:
        try:
            # if pattern captures two groups (key and value), preserve key and redact value
            def repl(m):
                if m.lastindex and m.lastindex >= 2:
                    return m.group(1) + ": " + REDACTION_TEXT
                else:
                    return REDACTION_TEXT
            s = p.sub(repl, s)
        except re.error:
            continue
    return s
