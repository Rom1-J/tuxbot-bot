"""
Starter file
"""
import asyncio
import os
import traceback
from distutils.util import strtobool

from ddtrace.profiling.profiler import Profiler

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
    with open("misc/logo.txt", encoding="UTF-8") as f:
        logo = f.read()

    print(logo)
    logger.info(
        "[C%s] Process %d online.", os.getenv("CLUSTER_ID"), os.getpid()
    )

    options: dict[str, str | int | None] = {}

    if shard_id := os.getenv("SHARD_ID"):
        options["shard_id"] = int(shard_id)

    if cluster_id := os.getenv("CLUSTER_ID"):
        options["cluster_id"] = int(cluster_id)

    if shard_count := os.getenv("SHARD_COUNT"):
        options["shard_count"] = int(shard_count)

    if cluster_count := os.getenv("CLUSTER_COUNT"):
        options["cluster_count"] = int(cluster_count)

    if first_shard_id := os.getenv("FIRST_SHARD_ID"):
        options["first_shard_id"] = int(first_shard_id)
        options["last_shard_id"] = os.getenv("LAST_SHARD_ID", None)

    if env == "development":
        from rich.traceback import install

        install(show_locals=True)

    tuxbot = None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        tuxbot = Tuxbot(options)
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
