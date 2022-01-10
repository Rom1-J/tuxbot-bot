"""
Starter file
"""
import asyncio
import os
import traceback

from tuxbot.core.Tuxbot import Tuxbot
from tuxbot.core.logger import logger


env = os.getenv("PYTHON_ENV", "production")


async def run_bot(tuxbot: Tuxbot) -> None:
    """Run the instance

    Parameters
    ----------
    tuxbot:Tuxbot
        Tuxbot instance
    """
    try:
        await tuxbot.launch()
    except Exception as e:
        if env == "development":
            traceback.print_exc()

        Tuxbot.crash_report(tuxbot, e)


def start():
    """Start function"""
    with open("logo.txt", "r") as f:
        logo = f.read()

    print(logo)
    logger.info(f"[C{os.getenv('clusterId')}] Process {os.getgid()} online.")

    options = {}

    if shard_id := os.getenv("shardId"):
        options["shard_id"] = int(shard_id)

    if cluster_id := os.getenv("clusterId"):
        options["cluster_id"] = int(cluster_id)

    if shard_count := os.getenv("shardCount"):
        options["shard_count"] = int(shard_count)

    if cluster_count := os.getenv("clusterCount"):
        options["cluster_count"] = int(cluster_count)

    if first_shard_id := os.getenv("firstShardId"):
        options["first_shard_id"] = int(first_shard_id)
        options["last_shard_id"] = os.getenv("lastShardId", None)

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

        Tuxbot.crash_report(tuxbot, e)


if __name__ == '__main__':
    start()
