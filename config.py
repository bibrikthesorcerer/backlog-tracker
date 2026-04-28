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
    

class _Django:
    secret_key: str
    debug: bool
    allowed_hosts: list
    cookies_secure: bool


class _Settings:
    POSTGRES: _Postgres
    PAGINATION: _Pagination
    DJANGO: _Django


proj_settings = cast(_Settings, Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['.secrets.toml'],
))

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
