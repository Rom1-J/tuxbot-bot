"""
Tuxbot core module: logger

Logger to format discord and tuxbot logs
"""
import logging
from logging.config import fileConfig

from pythonjsonlogger import jsonlogger
import sentry_sdk
from rich.logging import RichHandler

from tuxbot.core.config import config


# noinspection PyMissingOrEmptyDocstring
class Logger(logging.Logger):
    """Tuxbot logger"""
    def __init__(self):
        super(Logger, self).__init__("tuxbot")

        formatter = jsonlogger.JsonFormatter()
        fileConfig("logging.ini")

        json_handler = logging.FileHandler(filename="logs/logs.json")
        json_handler.setFormatter(formatter)

        self.addHandler(json_handler)
        self.addHandler(RichHandler(rich_tracebacks=True, tracebacks_show_locals=True))

        if dsn := config["sentry"].get("dsn"):
            sentry_sdk.init(dsn=dsn)


logger = Logger()
prom = object
