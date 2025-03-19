import json
import logging
import os
import sys
from enum import Enum

import structlog
from app.db.session import SessionLocal
from structlog.contextvars import merge_contextvars
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)

logger = structlog.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


class LogFormat(str, Enum):
    JSON = "json"
    CONSOLE = "console"


log_level = os.environ.get("LOG_LEVEL", logging.INFO)
if isinstance(log_level, str):
    log_level = log_level.upper()

logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

log_format = LogFormat(os.environ.get("LOG_FORMAT", default=LogFormat.JSON.value))

if log_format == LogFormat.JSON:
    renderer = structlog.processors.JSONRenderer(serializer=json.dumps)
else:
    renderer = structlog.dev.ConsoleRenderer()

structlog.configure(
    processors=[
        merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        renderer,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
