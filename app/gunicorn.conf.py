import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120

accesslog = "-"
errorlog = "-"
loglevel = "info"

wsgi_app = "myproject.wsgi:application"

limit_request_line = 4094
limit_request_fields = 100

proc_name = "gunicorn_myproject"

keepalive = 5

preload_app = True if os.getenv('PRELOAD_APP', '0') == '1' else False