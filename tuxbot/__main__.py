import argparse
import asyncio
import logging
import signal
import sys

import discord
from colorama import Fore, init, Style

import tuxbot.logging
from tuxbot.core import data_manager

log = logging.getLogger("tuxbot.main")
init()


def parse_cli_flags(args):
    parser = argparse.ArgumentParser(
        description="Tuxbot - OpenSource bot",
        usage="tuxbot <instance_name> [arguments]"
    )
    parser.add_argument("--version", "-V", help="Show tuxbot's used version")
    parser.add_argument("--list-instances", "-L",
                        help="List all instance names")
    parser.add_argument(
        "instance_name", nargs="?",
        help="Name of the bot instance created during `redbot-setup`.")

    args = parser.parse_args(args)

    if args.prefix:
        args.prefix = sorted(args.prefix, reverse=True)
    else:
        args.prefix = []

    return args


async def shutdown_handler(tux, signal_type, exit_code=None):
    if signal_type:
        log.info("%s received. Quitting...", signal_type)
        sys.exit(0)
    elif exit_code is None:
        log.info("Shutting down from unhandled exception")
        tux._shutdown_mode = 1

    if exit_code is not None:
        tux._shutdown_mode = exit_code

    try:
        await tux.logout()
    finally:
        pending = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)


async def run_bot(tux: Tuxbot, cli_flags: argparse.Namespace) -> None:
    data_path = data_manager.get_data_path(tuxbot.instance_name)

    tuxbot.logging.init_logging(
        level=cli_flags.logging_level,
        location=data_path / "logs"
    )

    log.debug("====Basic Config====")
    log.debug("Data Path: %s", data_path)

    if cli_flags.token:
        token = cli_flags.token
    else:
        token = await tux._config.token()

    if not token:
        log.critical("Token must be set if you want to login.")
        sys.exit(1)

    try:
        await tux.start(token, bot=True, cli_flags=cli_flags)
    except discord.LoginFailure:
        log.critical("This token appears to be valid.")
        sys.exit(1)

    return None


def main():
    tux = None
    cli_flags = parse_cli_flags(sys.argv[1:])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        if cli_flags.no_instance:
            print(Fore.RED
                  + "No instance provided ! "
                    "You can use 'tuxbot -L' to list all available instances"
                  + Style.RESET_ALL)
            sys.exit(1)

        tux = Tuxbot(
            cli_flags=cli_flags,
            description="Tuxbot, made from and for OpenSource",
            dm_help=None
        )

        loop.run_until_complete(run_bot(tux, cli_flags))
    except KeyboardInterrupt:
        log.warning("Please use <prefix>quit instead of Ctrl+C to Shutdown!")
        log.error("Received KeyboardInterrupt")
        if tuxbot is not None:
            loop.run_until_complete(shutdown_handler(tux, signal.SIGINT))
    except SystemExit as exc:
        log.info("Shutting down with exit code: %s", exc.code)
        if tuxbot is not None:
            loop.run_until_complete(shutdown_handler(tux, None, exc.code))
    except Exception as exc:
        log.exception("Unexpected exception (%s): ", type(exc), exc_info=exc)
        if tuxbot is not None:
            loop.run_until_complete(shutdown_handler(tux, None, 1))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        log.info("Please wait, cleaning up a bit more")
        loop.run_until_complete(asyncio.sleep(2))
        asyncio.set_event_loop(None)
        loop.stop()
        loop.close()
        exit_code = 1 if tuxbot is None else tux._shutdown_mode
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
