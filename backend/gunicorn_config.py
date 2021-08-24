import multiprocessing
import uvicorn

debug = False
reload = True
loglevel = 'debug'
bind = 'unix:/home/ftpuser/10002-TikTokTeenBackend/gunicorn/gunicorn.sock'
pidfile = '/home/ftpuser/10002-TikTokTeenBackend/gunicorn/gunicorn.pid'
logfile = '/home/ftpuser/10002-TikTokTeenBackend/gunicorn/debug.log'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker' 