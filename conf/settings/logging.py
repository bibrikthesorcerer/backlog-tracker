from config import proj_settings
from conf.settings.django import BASE_DIR


LOG_REQUESTS = True
LOG_USER_ATTRIBUTE = "username"
NO_REQUEST_ID = "no ID"
LOGGING_ENABLED = proj_settings.get("LOGGING.logging_enabled", True)
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True) #
if LOGGING_ENABLED:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'request_id': {
                '()': 'log_request_id.filters.RequestIDFilter'
            },
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        'formatters': {
            'standart': {
                'format': '{levelname:8} [{asctime}] [{request_id}] {name}: {message}',
                'style': '{'
            },
            'rich': {
                'format': '[{asctime}] [bold white on cyan]\\[{request_id}][/] [bold magenta]{name}[/]: {message}',
                'style': '{'
            },
        },
        'handlers': {
            'console': {
                'level': proj_settings.get("LOGGING.log_level", "INFO"),
                'filters': ['request_id'],
                'formatter': 'rich',
                # rich handler settings
                'class': 'rich.logging.RichHandler',
                'show_time': False,
                'rich_tracebacks': True,
                'markup': True
            },
            'file': {
                'level': proj_settings.get("LOGGING.log_level", "INFO"),
                'filters': ['request_id'],
                'formatter': 'standart',
                'class': 'logging.FileHandler',
                'filename': LOG_DIR / "debug.log",
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': proj_settings.get("LOGGING.django_log_level", "INFO"),
                'propagate': True
            },
            'django.db.backends': {
                'handlers': ['console', 'file'],
                'filters': ['require_debug_true'],
                'level': proj_settings.get("LOGGING.db_log_level", "WARNING"),
                'propagate': False
            },
        },
    }