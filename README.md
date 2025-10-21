
# logguard

`logguard` is a small utility to help automatically redact sensitive data from logs.

## Features (prototype)
- Redact based on a large seed list of sensitive field names (sensitive_keys.txt)
- Regex-based detection for emails, credit-card-like numbers, SSNs, IBAN-ish tokens
- `RedactingFormatter` for use with Python `logging`
- `@filter` decorator which patches `logging.info/debug/...` to apply redaction

## Quick start
```py
import logging
from logguard import RedactingFormatter, filter, redact

handler = logging.StreamHandler()
handler.setFormatter(RedactingFormatter("%(levelname)s: %(message)s"))
logger = logging.getLogger("demo")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User signed in: email=user@example.com, password=secret123")
# Output: INFO: User signed in: email=[REDACTED], password: [REDACTED]

@filter
def do_work():
    logging.info("api_key=abcd1234")
do_work()
```

## Packaging
This repo contains a `pyproject.toml` for a minimal build using `setuptools` (source distribution).

## Notes
This is a prototype. Production usage should consider:
- Thread safety of the decorator-based patching
- Avoiding over-redaction of safe fields
- Performance tuning for high-throughput logging
- Better tests and CI pipeline
