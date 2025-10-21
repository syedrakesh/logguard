import logging
from logguard import RedactingFormatter, filter

handler = logging.StreamHandler()
handler.setFormatter(RedactingFormatter("%(levelname)s: %(message)s"))
logger = logging.getLogger("demo")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("email=user@example.com")
logger.info("User signed in: email=user@example.com, password=secret123, api_key=abcd-1234-efgh, token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
logger.info("Payment info: card=4111-1111-1111-1111, uuid=550e8400-e29b-41d4-a716-446655440000, aws=AKIA1234567890ABCDEF")

@filter
def do_work():
    logging.info("This contains a secret: client_secret=verysecret")

do_work()
