import multiprocessing
import os

# point to wsgi app
wsgi_app = "conf.wsgi:application"

# number of workers
workers = int(
    os.environ.get(
        "GUNICORN_WORKERS",
        multiprocessing.cpu_count() * 2 + 1,
    )
)
# NOTE: later may switch to gthread for lower memory consumption inside a container
worker_class = "sync" 

# TCP + docker networking
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# docker handles supervision, no daemon needed
daemon = False

# worker restart
max_requests = 1000
max_requests_jitter = 50

timeout = int(os.environ.get("GUNICORN_TIMEOUT", 30))
graceful_timeout = int(
    os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", 30)
)
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", 2))

proc_name = "gunicorn_backlog"
preload_app = False

# docker performance magic
worker_tmp_dir = "/dev/shm"

# control socket not needed
control_socket_disable = True