from celery import Celery
from app.core.config import settings

if settings.REDIS_URL:
    celery_app = Celery("worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
else:
    # Local mode: Eager execution (synchronous)
    celery_app = Celery("worker", broker="memory://", backend="memory://")
    celery_app.conf.task_always_eager = True

celery_app.conf.task_routes = {
    "app.worker.tasks.*": "main-queue"
}
