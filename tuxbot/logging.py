import logging.handlers
import logging
import pathlib
import sys

MAX_OLD_LOGS = 8
MAX_BYTES = 5_000_000

formatter = logging.Formatter(
    "[{asctime}] [{levelname}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


def _setup_logging(level: int, location: pathlib.Path, name: str) -> None:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger_file = location / f"{name}.log"

    handler = logging.handlers.RotatingFileHandler(
        str(logger_file.resolve()),
        maxBytes=MAX_BYTES,
        backupCount=MAX_OLD_LOGS,
    )

    base_handler = logging.handlers.RotatingFileHandler(
        str(logger_file.resolve()),
        maxBytes=MAX_BYTES,
        backupCount=MAX_OLD_LOGS,
    )

    handler.setFormatter(formatter)
    base_handler.setFormatter(formatter)


def init_logging(level: int, location: pathlib.Path) -> None:
    """Initialize loggers.

    Parameters
    ----------
    level:int
        Level of debug.
    location:Path
        Where to store Logs.
    """

    _setup_logging(level, location, "discord")
    _setup_logging(level, location, "tuxbot")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
