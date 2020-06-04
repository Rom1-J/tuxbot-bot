import argparse
import asyncio
import getpass
import json
import logging
import platform
import signal
import sys
from argparse import Namespace
from typing import NoReturn

import discord
import pip
from colorama import Fore, init, Style
from pip._vendor import distro

import tuxbot.logging
from tuxbot.core import data_manager
from tuxbot.core.bot import Tux, ExitCodes
from tuxbot.core.utils.functions.cli import bordered
from . import __version__

log = logging.getLogger("tuxbot.main")
init()


def list_instances() -> NoReturn:
    """List all available instances

    """
    with data_manager.config_file.open() as fs:
        datas = json.load(fs)

    instances = list(datas.keys())

    info = {
        'title': "Instances",
        'rows': []
    }

    for instance in instances:
        info['rows'].append(f"-> {instance}")

    print(bordered(info))
    sys.exit(0)


def debug_info() -> NoReturn:
    """Show debug infos relatives to the bot

    """
    python_version = sys.version.replace('\n', '')
    pip_version = pip.__version__
    tuxbot_version = __version__
    dpy_version = discord.__version__

    os_info = distro.linux_distribution()
    os_info = f"{os_info[0]} {os_info[1]}"

    runner = getpass.getuser()

    info = {
        'title': "Debug Info",
        'rows': [
            f"Tuxbot version: {tuxbot_version}",
            "",
            f"Python version: {python_version}",
            f"Python executable path: {sys.executable}",
            f"Pip version: {pip_version}",
            f"Discord.py version: {dpy_version}",
            "",
            f"OS info: {os_info}",
            f"System arch: {platform.machine()}",
            f"User: {runner}",
        ]
    }

    print(bordered(info))
    sys.exit(0)


def parse_cli_flags(args: list) -> Namespace:
    """Parser for cli values.

    Parameters
    ----------
    args:list
        Is a list of all passed values.
    Returns
    -------
    Namespace
    """
    parser = argparse.ArgumentParser(
        description="Tuxbot - OpenSource bot",
        usage="tuxbot <instance_name> [arguments]"
    )
    parser.add_argument(
        "--version", "-V",
        action="store_true",
        help="Show tuxbot's used version"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show debug information."
    )
    parser.add_argument(
        "--list-instances", "-L",
        action="store_true",
        help="List all instance names"
    )
    parser.add_argument(
        "--token", "-T",
        type=str,
        help="Run Tuxbot with passed token"
    )
    parser.add_argument(
        "instance_name", nargs="?",
        help="Name of the bot instance created during `tuxbot-setup`."
    )

    args = parser.parse_args(args)

    return args


async def shutdown_handler(tux: Tux, signal_type, exit_code=None) -> NoReturn:
    """Handler when the bot shutdown

    It cancels all running task.

    Parameters
    ----------
    tux:Tux
        Object for the bot.
    signal_type:int, None
        Exiting signal code.
    exit_code:None|int
        Code to show when exiting.
    """
    if signal_type:
        log.info("%s received. Quitting...", signal_type)
        sys.exit(ExitCodes.SHUTDOWN)
    elif exit_code is None:
        log.info("Shutting down from unhandled exception")
        tux.shutdown_code = ExitCodes.CRITICAL

    if exit_code is not None:
        tux.shutdown_code = exit_code

    try:
        await tux.logout()
    finally:
        pending = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)


async def run_bot(tux: Tux, cli_flags: Namespace, loop) -> None:
    """This run the bot.

    Parameters
    ----------
    tux:Tux
        Object for the bot.
    cli_flags:Namespace
        All different flags passed in the console.

    Returns
    -------
    None
        When exiting, this function return None.
    """
    data_path = data_manager.data_path(tux.instance_name)

    tuxbot.logging.init_logging(
        10,
        location=data_path / "logs"
    )

    log.debug("====Basic Config====")
    log.debug("Data Path: %s", data_path)

    if cli_flags.token:
        token = cli_flags.token
    else:
        token = tux.config('core').get('token')

    if not token:
        log.critical("Token must be set if you want to login.")
        sys.exit(ExitCodes.CRITICAL)

    try:
        await tux.load_packages()
        await tux.start(token, bot=True)
    except discord.LoginFailure:
        log.critical("This token appears to be valid.")
        sys.exit(ExitCodes.CRITICAL)

    return None


def main() -> NoReturn:
    """Main function

    """
    tux = None
    cli_flags = parse_cli_flags(sys.argv[1:])

    if cli_flags.list_instances:
        list_instances()
    elif cli_flags.debug:
        debug_info()
    elif cli_flags.version:
        print("Tuxbot V3")
        print(f"Complete Version: {__version__}")
        sys.exit(0)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        if not cli_flags.instance_name:
            print(Fore.RED
                  + "No instance provided ! "
                    "You can use 'tuxbot -L' to list all available instances"
                  + Style.RESET_ALL)
            sys.exit(ExitCodes.CRITICAL)

        tux = Tux(
            cli_flags=cli_flags,
            description="Tuxbot, made from and for OpenSource",
            dm_help=None
        )

        loop.run_until_complete(run_bot(tux, cli_flags, loop))
    except KeyboardInterrupt:
        print(Fore.RED
              + "Please use <prefix>quit instead of Ctrl+C to Shutdown!"
              + Style.RESET_ALL)
        log.warning("Please use <prefix>quit instead of Ctrl+C to Shutdown!")
        log.error("Received KeyboardInterrupt")
        if tux is not None:
            loop.run_until_complete(shutdown_handler(tux, signal.SIGINT))
    except SystemExit as exc:
        log.info("Shutting down with exit code: %s", exc.code)
        if tux is not None:
            loop.run_until_complete(shutdown_handler(tux, None, exc.code))
    except Exception as exc:
        log.exception("Unexpected exception (%s): ", type(exc), exc_info=exc)
        if tux is not None:
            loop.run_until_complete(shutdown_handler(tux, None, 1))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        log.info("Please wait, cleaning up a bit more")
        loop.run_until_complete(asyncio.sleep(1))
        asyncio.set_event_loop(None)
        loop.stop()
        loop.close()
        exit_code = ExitCodes.CRITICAL if tux is None else tux.shutdown_code
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
