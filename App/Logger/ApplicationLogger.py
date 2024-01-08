import logging
import os
from functools import wraps

from App.Config import basedir


class ApplicationLogger:
    def __init__(self, log_level=logging.INFO, max_log_size_kb=65):
        self.log_level = log_level
        self.max_log_size_kb = max_log_size_kb
        self.setup_logger()

    def setup_logger(self):
        logs_dir = os.path.join(basedir, "Logger", "logs")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        self.log_file = os.path.join(logs_dir, "app.log")
        self.logger = logging.getLogger("ApplicationLogger")
        self.logger.setLevel(self.log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def rotate_log_file(self):
        if os.path.exists(self.log_file):
            log_size = os.path.getsize(self.log_file)
            if log_size > self.max_log_size_kb * 1024:
                new_log_file = os.path.join(
                    os.path.dirname(self.log_file), "app_old.log"
                )
                os.rename(self.log_file, new_log_file)

    def log_info(self, message):
        self.rotate_log_file()
        self.logger.info(message)

    def log_warning(self, message):
        self.rotate_log_file()
        self.logger.warning(message)

    def log_error(self, message):
        self.rotate_log_file()
        self.logger.error(message)

    def log_exception(self, message):
        self.rotate_log_file()
        self.logger.exception(f"\n{message}\n")

    def exception_handler(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_exception(f"Exception in {func.__name__}: {str(e)}")

        return wrapper