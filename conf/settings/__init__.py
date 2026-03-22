from split_settings.tools import include

include(
    './django.py',
    './database.py',
)

import dynaconf  # noqa
settings = dynaconf.DjangoDynaconf(__name__)  # noqa