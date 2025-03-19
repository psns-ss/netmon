import asyncio
from typing import List

import sentry_sdk
import structlog
from app import crud, models
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[CeleryIntegration()])

logger = structlog.get_logger()


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def check_all_machines() -> None:
    logger.debug("started check machine statuses")
    skip = 0
    limit = 100
    db = SessionLocal()
    try:
        while True:
            checked_machines: List[models.Machine] = asyncio.run(
                crud.machine.get_multi_with_check_online(db, skip=skip, limit=limit)
            )

            if not checked_machines:
                break

            logger.debug(f"checked {len(checked_machines)} machines")

            for ma in checked_machines:
                asyncio.run(crud.machine_process.get_multi_with_poll(db, ma.id))

            skip += limit

        logger.debug("checked all machines")
    finally:
        db.close()
