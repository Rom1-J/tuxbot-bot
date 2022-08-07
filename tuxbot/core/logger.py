"""
Tuxbot core module: logger

Logger to format discord and tuxbot logs
"""
import logging

import sentry_sdk
from pythonjsonlogger import jsonlogger
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
        "dd.env",
        "dd.service",
        "dd.version",
        "dd.trace_id",
        "dd.span_id",
    ]

    def __init__(self) -> None:
        super().__init__(
            "tuxbot", level=config.get("log_level", "info").upper()
        )

        custom_format = " ".join([f"%({i:s})s" for i in self.keys])
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
