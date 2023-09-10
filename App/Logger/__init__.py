import os
import logging
from functools import wraps
from App.Config import basedir


class ApplicationLogger:
    def __init__(self, log_level=logging.INFO):
        logs_dir = os.path.join(basedir, 'Logger', 'Logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        self.log_file = os.path.join(logs_dir, 'app.log')
        self.logger = logging.getLogger("ApplicationLogger")
        self.logger.setLevel(log_level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_exception(self, message):
        self.logger.exception(f'\n{message}\n')

    def exception_handler(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_exception(f"Exception in {func.__name__}: {str(e)}")
        return wrapper
