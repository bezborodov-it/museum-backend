import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("museum_api")
    logger.setLevel(logging.INFO)

    log_format = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d: %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_dir = os.getenv("LOG_DIR", "./logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "museum_api.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.getLogger("uvicorn").handlers = logger.handlers
    logging.getLogger("uvicorn.error").handlers = logger.handlers
    logging.getLogger("uvicorn.access").handlers = logger.handlers


    return logger