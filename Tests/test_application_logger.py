import logging
import os

import pytest

from App.Logger import ApplicationLogger

log_file_path = os.path.join(os.path.dirname(__file__), "../App/Logger/logs/app.log")

test_logger = ApplicationLogger(log_level=logging.DEBUG)


def test_log_info():
    test_message = "This is a test message."
    test_logger.log_info(test_message)
    with open(log_file_path, "r") as log_file:
        log_contents = log_file.read()
        assert test_message in log_contents


def test_log_warning():
    test_message = "This is a test warning."
    test_logger.log_warning(test_message)

    with open(log_file_path, "r") as log_file:
        log_contents = log_file.read()
        assert test_message in log_contents


def test_log_error():
    test_message = "This is a test error."

    test_logger.log_error(test_message)

    with open(log_file_path, "r") as log_file:
        log_contents = log_file.read()
        assert test_message in log_contents


def test_log_exception():
    test_message = "This is a test exception."

    test_logger.log_exception(test_message)

    with open(log_file_path, "r") as log_file:
        log_contents = log_file.read()
        assert test_message in log_contents


if __name__ == "__main__":
    pytest.main()
