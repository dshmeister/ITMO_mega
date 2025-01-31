# import json
# import multiprocessing
# import os
#
# workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
# max_workers_str = os.getenv("MAX_WORKERS")
# use_max_workers = None
# if max_workers_str:
#     use_max_workers = int(max_workers_str)
# web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
#
# host = os.getenv("HOST", "0.0.0.0")
# port = os.getenv("PORT", "9001")
# bind_env = os.getenv("BIND", None)
# use_loglevel = os.getenv("LOG_LEVEL", "info")
# if bind_env:
#     use_bind = bind_env
# else:
#     use_bind = f"{host}:{port}"
#
# cores = multiprocessing.cpu_count()
# workers_per_core = float(workers_per_core_str)
# default_web_concurrency = workers_per_core * cores
# if web_concurrency_str:
#     web_concurrency = int(web_concurrency_str)
#     assert web_concurrency > 0
# else:
#     web_concurrency = max(int(default_web_concurrency), 2)
#     if use_max_workers:
#         web_concurrency = min(web_concurrency, use_max_workers)
# accesslog_var = os.getenv("ACCESS_LOG", "-")
# use_accesslog = accesslog_var or None
# errorlog_var = os.getenv("ERROR_LOG", "-")
# use_errorlog = errorlog_var or None
# graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "60")
# timeout_str = os.getenv("TIMEOUT", "120")
# keepalive_str = os.getenv("KEEP_ALIVE", "15")
#
# # Gunicorn config variables
# loglevel = use_loglevel
# workers = web_concurrency
# bind = use_bind
# errorlog = use_errorlog
# worker_tmp_dir = "/dev/shm"
# accesslog = use_accesslog
# graceful_timeout = int(graceful_timeout_str)
# timeout = int(timeout_str)
# keepalive = int(keepalive_str)
#
#
# # For debugging and testing
# log_data = {
#     "loglevel": loglevel,
#     "workers": workers,
#     "bind": bind,
#     "graceful_timeout": graceful_timeout,
#     "timeout": timeout,
#     "keepalive": keepalive,
#     "errorlog": errorlog,
#     "accesslog": accesslog,
#     # Additional, non-gunicorn variables
#     "workers_per_core": workers_per_core,
#     "use_max_workers": use_max_workers,
#     "host": host,
#     "port": port,
# }
# print(json.dumps(log_data))
#



import json
import multiprocessing
import os
import math

cpu_cores = multiprocessing.cpu_count()
workers = min(math.ceil(cpu_cores / 2), 16)  # До 6 воркеров максимум

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "9001")
bind = os.getenv("BIND", f"{host}:{port}")

loglevel = os.getenv("LOG_LEVEL", "info")
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")

# Таймауты
timeout = 1200
graceful_timeout = 360 # Даем воркерам больше времени на завершение
keepalive = 120  # Улучшаем повторное использование соединений

# Перезапуск воркеров при утечке памяти
max_requests = workers * 2000  # Динамический лимит запросов
max_requests_jitter = 500

# 🏃‍♂️ Используем асинхронный обработчик
worker_class = "uvicorn.workers.UvicornWorker"
worker_tmp_dir = "/tmp"  # Надежнее, чем /dev/shm
preload_app = True  # Оптимизируем загрузку

log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    "cpu_cores": cpu_cores,
    "max_requests": max_requests,
    "max_requests_jitter": max_requests_jitter,
    "preload_app": preload_app,
}

print(json.dumps(log_data))
