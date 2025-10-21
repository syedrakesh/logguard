
import logging
from logguard import RedactingFormatter, filter

handler = logging.StreamHandler()
handler.setFormatter(RedactingFormatter("%(levelname)s: %(message)s"))
logger = logging.getLogger("demo")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User signed in: email=user@example.com, password=secret123, api_key=abcd-1234-efgh")

@filter
def do_work():
    logging.info("This contains a secret: client_secret=verysecret")
do_work()
