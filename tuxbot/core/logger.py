"""
Tuxbot core module: logger

Logger to format discord and tuxbot logs
"""
import logging

from pythonjsonlogger import jsonlogger
import sentry_sdk
from rich.logging import RichHandler

from tuxbot.core.config import config


class Logger(logging.Logger):
    """Tuxbot logger"""

    keys = [
        "asctime",
        "created",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "thread",
        "threadName",
    ]

    def __init__(self):
        super().__init__("tuxbot")

        custom_format = " ".join(["%({0:s})s".format(i) for i in self.keys])
        formatter = jsonlogger.JsonFormatter(custom_format)

        json_handler = logging.FileHandler(
            filename=str(
                config["paths"]["cwd"] / "data" / "logs" / "logs.json"
            )
        )
        json_handler.setFormatter(formatter)

        self.addHandler(json_handler)

        if config["test"]:
            self.addHandler(
                RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)
            )
        elif dsn := config["sentry"].get("dsn"):
            # pylint: disable=abstract-class-instantiated
            sentry_sdk.init(dsn=dsn)


logger = Logger()
prom = object
