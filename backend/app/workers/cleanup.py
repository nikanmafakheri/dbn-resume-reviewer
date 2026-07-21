"""Periodic cleanup tasks."""

import logging
from app.workers.celery import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def cleanup_stale_uploads():
    """Delete media files older than 24h with no linked resume record."""
    logger.info("Running stale upload cleanup")
    # TODO: implement
