"""
Tuxbot core module: logger

Logger to format discord and tuxbot logs
"""
import logging

import sentry_sdk
from pythonjsonlogger import jsonlogger
from rich.console import Console
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
        log_level = config.LOG_LEVEL
        log_path = "logs"

        super().__init__("tuxbot", level=log_level)

        discord_logger = logging.getLogger("discord")
        # discord_logger.setLevel(log_level)

        custom_format = " ".join([f"%({i:s})s" for i in self.keys])
        formatter = jsonlogger.JsonFormatter(custom_format)

        bot_handler = logging.FileHandler(filename=f"{log_path}/logs.json")
        bot_handler.setFormatter(formatter)
        self.addHandler(bot_handler)

        discord_handler = logging.FileHandler(
            filename=f"{log_path}/discord.json"
        )
        discord_handler.setFormatter(formatter)
        discord_logger.addHandler(discord_handler)

        if log_level == logging.DEBUG:
            test_handler = RichHandler(
                console=Console(width=206),
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                tracebacks_width=None,
            )

            self.addHandler(test_handler)
            discord_logger.addHandler(test_handler)
            discord_logger.addHandler(discord_handler)
        elif dsn := config.SENTRY_DSN:
            # pylint: disable=abstract-class-instantiated
            sentry_sdk.init(dsn=dsn)


logger = Logger()
