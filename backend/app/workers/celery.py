"""Celery app configuration."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "dbn_resume_reviewer",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_soft_time_limit=300,
    task_hard_time_limit=330,
    task_acks_late=True,
    worker_concurrency=4,
)

# Auto-discover tasks in the workers package
celery_app.autodiscover_tasks(["app.workers"])

# Recurring housekeeping: sweep stale uploads hourly (only meaningful when
# celery-beat is running, which docker-compose starts).
celery_app.conf.beat_schedule = {
    "cleanup-stale-uploads": {
        "task": "app.workers.cleanup.cleanup_stale_uploads",
        "schedule": 3600.0,
    },
}
