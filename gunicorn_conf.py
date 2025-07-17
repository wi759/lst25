import multiprocessing

# Server socket
bind = "0.0.0.0:8000"

# Change working directory
chdir = "/app/backend"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
accesslog = "-"
errorlog = "-"
