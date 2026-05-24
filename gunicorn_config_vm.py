import multiprocessing

# point to wsgi app
wsgi_app = "conf.wsgi:application"

# number of workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# unix socket to talk to nginx
bind = "unix:./app.sock"

accesslog = "-"
errorlog = "-"
loglevel = "info"

# systemd is present, no daemon needed
daemon = False

# worker restart
max_requests = 1000
max_requests_jitter = 50

timeout = 30
graceful_timeout = 30
keepalive = 2

# perms for socket
umask = 0o007

preload_app = True