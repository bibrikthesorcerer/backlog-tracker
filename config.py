from dynaconf import Dynaconf
from typing import cast


class _Postgres:
    name: str
    user: str
    password: str
    host: str
    port: str


class _Pagination:
    media_items: int
    queue_N: int
    

class _Django:
    secret_key: str
    debug: bool
    allowed_hosts: list
    cookies_secure: bool


class _Logging:
    logging_enabled: bool
    log_level: str
    django_log_level: str
    db_log_level: str



class _Settings:
    POSTGRES: _Postgres
    PAGINATION: _Pagination
    DJANGO: _Django
    LOGGING: _Logging


proj_settings = cast(_Settings, Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['.secrets.toml'],
))

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
