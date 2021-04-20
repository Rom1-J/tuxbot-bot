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


def init_logging(level: int, location: pathlib.Path) -> None:
    """Initialize loggers.

    Parameters
    ----------
    level:int
        Level of debug.
    location:Path
        Where to store Logs.
    """

    # dpy_logger = logging.getLogger("discord")
    # dpy_logger.setLevel(logging.WARN)
    # dpy_logger_file = location / "discord.log"

    base_logger = logging.getLogger("tuxbot")
    base_logger.setLevel(level)
    base_logger_file = location / "tuxbot.log"

    # dpy_handler = logging.handlers.RotatingFileHandler(
    #     str(dpy_logger_file.resolve()),
    #     maxBytes=MAX_BYTES,
    #     backupCount=MAX_OLD_LOGS,
    # )
    base_handler = logging.handlers.RotatingFileHandler(
        str(base_logger_file.resolve()),
        maxBytes=MAX_BYTES,
        backupCount=MAX_OLD_LOGS,
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    # dpy_handler.setFormatter(formatter)
    base_handler.setFormatter(formatter)

    # dpy_logger.addHandler(dpy_handler)
    base_logger.addHandler(base_handler)
