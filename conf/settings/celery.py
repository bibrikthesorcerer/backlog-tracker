from config import proj_settings

CELERY_BROKER_URL = proj_settings.get(
    "CELERY.broker_url",
    "redis://localhost:6379/0"
)
CELERY_RESULT_BACKEND = proj_settings.get(
    "CELERY.result_backend",
    "redis://localhost:6379/1"
)
