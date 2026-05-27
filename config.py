from dynaconf import Dynaconf

proj_settings = Dynaconf(
    envvar_prefix="BL",
    env_switcher="BL_MODE",
    settings_files=[
        "settings.toml",
        ".secrets.toml",
        "settings.local.toml",
    ],
    load_dotenv=True,
    environments=True,
)