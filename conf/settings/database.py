from config import proj_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': proj_settings.POSTGRES.name,
        'USER': proj_settings.POSTGRES.user,
        'PASSWORD': proj_settings.POSTGRES.password,
        'HOST': proj_settings.POSTGRES.host,
        'PORT': proj_settings.POSTGRES.port,
    }
}