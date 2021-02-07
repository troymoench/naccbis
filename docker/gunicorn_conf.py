import multiprocessing

bind = "0.0.0.0:8000"
workers = 2
# workers = 2 * multiprocessing.cpu_count() + 1
accesslog = "-"
worker_tmp_dir = "/dev/shm"
worker_class = "uvicorn.workers.UvicornWorker"
# loglevel = "DEBUG"
