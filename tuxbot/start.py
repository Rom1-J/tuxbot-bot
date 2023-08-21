"""Starter file."""
import asyncio
import os
import traceback
from pathlib import Path

from tuxbot.core.config import config
from tuxbot.core.logger import logger
from tuxbot.core.tuxbot import Tuxbot


env = os.getenv("PYTHON_ENV", "production")


async def run_bot(tuxbot: Tuxbot) -> None:
    """
    Run the instance.

    Parameters
    ----------
    tuxbot: :class:`Tuxbot`
        Tuxbot instance
    """
    try:
        await tuxbot.launch()
    except Exception as e:  # noqa: BLE001
        if env == "development":
            traceback.print_exc()

        Tuxbot.crash_report(tuxbot, e)


def start() -> None:
    """Start function."""
    with Path.open(Path("tuxbot/misc/logo.txt")) as f:
        logo = f.read()

    logger.info(logo)
    logger.info("[C%s] Process %d online.", config.CLUSTER_ID, os.getpid())

    if env == "development":
        from rich.traceback import install

        install(show_locals=True)

    tuxbot = None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        tuxbot = Tuxbot()
        loop.run_until_complete(run_bot(tuxbot))
    except KeyboardInterrupt:
        if tuxbot is not None:
            loop.run_until_complete(tuxbot.shutdown())
    except Exception as e:  # noqa: BLE001
        if env == "development":
            traceback.print_exc()

        if tuxbot:
            Tuxbot.crash_report(tuxbot, e)


if __name__ == "__main__":
    start()
