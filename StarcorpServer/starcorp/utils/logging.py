import os
import sys
import logging

from logging import StreamHandler
from logging.handlers import RotatingFileHandler

KB = 1024
MB = KB * 1024
GB = MB * 1024

LOGGER_NAME = "starcorp"
# create logger
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(logging.DEBUG)


# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create file handler and set level to debug
file_handler = RotatingFileHandler("starcorp.log", maxBytes=10 * MB, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
LOGGER.addHandler(file_handler)


if os.getenv("LOG_TO_CONSOLE") == "true":
    # create console handler and set level to debug
    console_handler = StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(console_handler)


def get_logger(name):
    return logging.getLogger(f"{LOGGER_NAME}.{name}")
