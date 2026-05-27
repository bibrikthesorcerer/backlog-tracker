from config import proj_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': proj_settings.get("POSTGRES.name", "backlog"),
        'USER': proj_settings.get("POSTGRES.user"),
        'PASSWORD': proj_settings.get("POSTGRES.password"),
        'HOST': proj_settings.get("POSTGRES.host", "localhost"),
        'PORT': proj_settings.get("POSTGRES.port", 5432),
    }
}