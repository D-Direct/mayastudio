"""
Celery Worker Configuration
Background tasks for audio generation and video rendering
"""

from celery import Celery
from app.config import settings

# Initialize Celery app
celery_app = Celery(
    "mayastudio",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.audio_generation",
        "app.tasks.video_rendering",
        "app.tasks.script_parsing",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max
    task_soft_time_limit=540,  # 9 minutes soft limit
)

# Optional: Task routes for prioritization
celery_app.conf.task_routes = {
    "app.tasks.audio_generation.*": {"queue": "audio"},
    "app.tasks.video_rendering.*": {"queue": "video"},
    "app.tasks.script_parsing.*": {"queue": "parsing"},
}

if __name__ == "__main__":
    celery_app.start()
