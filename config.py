from dynaconf import Dynaconf
from typing import cast


class _Postgres:
    name: str
    user: str
    password: str
    host: str
    port: str


class _Settings:
    POSTGRES: _Postgres


settings = cast(_Settings, Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['.secrets.toml'],
))

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
