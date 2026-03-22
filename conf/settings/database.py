from config import settings as dc_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': dc_settings.POSTGRES.name,
        'USER': dc_settings.POSTGRES.user,
        'PASSWORD': dc_settings.POSTGRES.password,
        'HOST': dc_settings.POSTGRES.host,
        'PORT': dc_settings.POSTGRES.port,
    }
}