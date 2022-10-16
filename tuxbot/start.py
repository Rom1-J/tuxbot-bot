"""
Starter file
"""
import asyncio
import os
import traceback
from distutils.util import strtobool

from ddtrace.profiling.profiler import Profiler

from tuxbot.core.config import config
from tuxbot.core.logger import logger
from tuxbot.core.Tuxbot import Tuxbot


env = os.getenv("PYTHON_ENV", "production")


async def run_bot(tuxbot: Tuxbot) -> None:
    """Run the instance

    Parameters
    ----------
    tuxbot: :class:`Tuxbot`
        Tuxbot instance
    """
    try:
        if env != "development" and strtobool(os.getenv("DD_ACTIVE", "false")):
            Profiler().start()  # type: ignore

        await tuxbot.launch()
    except Exception as e:
        if env == "development":
            traceback.print_exc()

        Tuxbot.crash_report(tuxbot, e)


def start() -> None:
    """Start function"""
    with open("tuxbot/misc/logo.txt", encoding="UTF-8") as f:
        logo = f.read()

    print(logo)
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
    except Exception as e:
        if env == "development":
            traceback.print_exc()

        if tuxbot:
            Tuxbot.crash_report(tuxbot, e)


if __name__ == "__main__":
    start()
