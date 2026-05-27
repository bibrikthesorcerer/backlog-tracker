import os
import sys
import django
from time import sleep
# load django env to load DB credentials + ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

# get logger
import logging
log = logging.getLogger(__name__)

from django.db import connections
from django.db.utils import OperationalError

# see if postgres is up'n'ready
MAX_RETRIES = int(os.environ.get("DB_CONN_MAX_RETRIES", 5))
connected = False
log.info("Waiting for PostgreSQL...")
for i in range(MAX_RETRIES):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
        log.info("Database ready.")
        connected = True
        break;
    except OperationalError as err:
        connections["default"].close()
        log.info(f"Connection attempt {i+1} failed...")
        sleep(5)


if not connected:
    log.error(f"PostgreSQL is unreachable after {MAX_RETRIES} attempts.")
    sys.exit(1)

# call migrations
from django.core.management import call_command
log.info("Applying migrations...")
call_command("migrate", interactive=False)
log.info("Migrations applied.")

# run gunicorn
log.info("Starting gunicorn...")
os.execvp(
    "python",
    [
        "python",
        "-m",
        "gunicorn",
        "-c",
        "gunicorn_config_docker.py",
        "conf.wsgi:application",
    ],
)