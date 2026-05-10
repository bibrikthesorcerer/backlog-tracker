from config import proj_settings

CELERY_BROKER_URL = proj_settings.CELERY.broker_url
CELERY_RESULT_BACKEND = proj_settings.CELERY.result_backend
