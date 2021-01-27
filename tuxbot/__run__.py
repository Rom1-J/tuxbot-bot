import argparse
import asyncio
import logging
import signal
import sys
import os
from argparse import Namespace
from datetime import datetime

import discord
import humanize
import pip
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table, box
from rich.text import Text
from rich import print as rprint

import tuxbot.logging
from tuxbot.core.bot import Tux
from tuxbot.core import config
from tuxbot.core.utils import data_manager
from tuxbot.core.utils.console import console
from . import __version__, version_info, ExitCodes

log = logging.getLogger("tuxbot.main")

BORDER_STYLE = "not dim"


def list_instances() -> None:
    """List all available instances"""
    app_config = config.ConfigFile(
        data_manager.config_dir / "config.yaml", config.AppConfig
    ).config

    console.print(
        Panel("[bold green]Instances", style="green"), justify="center"
    )
    console.print()

    columns = Columns(expand=True, padding=2, align="center")
    for instance, details in app_config.Instances.items():
        active = details["active"]
        last_run = (
            humanize.naturaltime(
                datetime.now() - datetime.fromtimestamp(details["last_run"])
            )
            or "[i]unknown"
        )

        table = Table(
            style="dim", border_style=BORDER_STYLE, box=box.HEAVY_HEAD
        )
        table.add_column("Name")
        table.add_column(("Running since" if active else "Last run"))
        table.add_row(instance, last_run)
        table.title = Text(instance, style="green" if active else "red")
        columns.add_renderable(table)
    console.print(columns)
    console.print()

    sys.exit(os.EX_OK)


def debug_info() -> None:
    """Show debug info relatives to the bot"""
    python_version = sys.version.replace("\n", "")
    pip_version = pip.__version__
    tuxbot_version = __version__
    dpy_version = discord.__version__

    uptime = os.popen("/usr/bin/uptime").read().strip().split()

    console.print(
        Panel("[bold blue]Debug Info", style="blue"), justify="center"
    )
    console.print()

    columns = Columns(expand=True, padding=2, align="center")

    table = Table(style="dim", border_style=BORDER_STYLE, box=box.HEAVY_HEAD)
    table.add_column(
        "Bot Info",
    )
    table.add_row(f"[u]Tuxbot version:[/u] {tuxbot_version}")
    table.add_row(f"[u]Major:[/u] {version_info.major}")
    table.add_row(f"[u]Minor:[/u] {version_info.minor}")
    table.add_row(f"[u]Micro:[/u] {version_info.micro}")
    table.add_row(f"[u]Level:[/u] {version_info.releaselevel}")
    table.add_row(f"[u]Last change:[/u] {version_info.info}")
    columns.add_renderable(table)

    table = Table(style="dim", border_style=BORDER_STYLE, box=box.HEAVY_HEAD)
    table.add_column(
        "Python Info",
    )
    table.add_row(f"[u]Python version:[/u] {python_version}")
    table.add_row(f"[u]Python executable path:[/u] {sys.executable}")
    table.add_row(f"[u]Pip version:[/u] {pip_version}")
    table.add_row(f"[u]Discord.py version:[/u] {dpy_version}")
    columns.add_renderable(table)

    table = Table(style="dim", border_style=BORDER_STYLE, box=box.HEAVY_HEAD)
    table.add_column(
        "Server Info",
    )
    table.add_row(f"[u]System:[/u] {os.uname().sysname}")
    table.add_row(f"[u]System arch:[/u] {os.uname().machine}")
    table.add_row(f"[u]Kernel:[/u] {os.uname().release}")
    table.add_row(f"[u]User:[/u] {os.getlogin()}")
    table.add_row(f"[u]Uptime:[/u] {uptime[2][:-1]}")
    table.add_row(
        f"[u]Load Average:[/u] {' '.join(map(str, os.getloadavg()))}"
    )
    columns.add_renderable(table)

    console.print(columns)
    console.print()

    sys.exit(os.EX_OK)


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
        usage="tuxbot <instance_name> [arguments]",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="store_true",
        help="Show tuxbot's used version",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show debug information."
    )
    parser.add_argument(
        "--list-instances",
        "-L",
        action="store_true",
        help="List all instance names",
    )
    parser.add_argument(
        "--token", "-T", type=str, help="Run Tuxbot with passed token"
    )
    parser.add_argument(
        "instance_name",
        nargs="?",
        help="Name of the bot instance created during `tuxbot-setup`.",
    )

    args = parser.parse_args(args)

    return args


async def shutdown_handler(tux: Tux, signal_type, exit_code=None) -> None:
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
    elif exit_code is None:
        log.info("Shutting down from unhandled exception")
        tux.shutdown_code = ExitCodes.CRITICAL

    if exit_code is not None:
        tux.shutdown_code = exit_code

    await tux.shutdown()


async def run_bot(tux: Tux, cli_flags: Namespace) -> None:
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

    tuxbot.logging.init_logging(10, location=data_path / "logs")

    log.debug("====Basic Config====")
    log.debug("Data Path: %s", data_path)

    if cli_flags.token:
        token = cli_flags.token
    else:
        token = tux.config.Core.token

    if not token:
        log.critical("Token must be set if you want to login.")
        sys.exit(ExitCodes.CRITICAL)

    try:
        await tux.load_packages()
        console.print()
        await tux.start(token=token, bot=True)
    except discord.LoginFailure:
        log.critical("This token appears to be valid.")
        console.print()
        console.print(
            "[prompt.invalid]This token appears to be valid. [i]exiting...[/i]"
        )
        sys.exit(ExitCodes.CRITICAL)
    except Exception as e:
        log.critical(e)
        raise e

    return None


def run() -> None:
    """Main function"""
    tux = None
    cli_flags = parse_cli_flags(sys.argv[1:])

    if cli_flags.list_instances:
        list_instances()
    elif cli_flags.debug:
        debug_info()
    elif cli_flags.version:
        rprint(f"Tuxbot V{version_info.major}")
        rprint(f"Complete Version: {__version__}")

        sys.exit(os.EX_OK)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        if not cli_flags.instance_name:
            console.print(
                "[red]No instance provided ! "
                "You can use 'tuxbot -L' to list all available instances"
            )
            sys.exit(ExitCodes.CRITICAL)

        tux = Tux(
            cli_flags=cli_flags,
            description="Tuxbot, made from and for OpenSource",
            dm_help=None,
        )

        loop.run_until_complete(run_bot(tux, cli_flags))
    except KeyboardInterrupt:
        console.print(
            "  [red]Please use <prefix>quit instead of Ctrl+C to Shutdown!"
        )
        log.warning("Please use <prefix>quit instead of Ctrl+C to Shutdown!")
        log.info("Received KeyboardInterrupt")
        console.print("[i]Trying to shutdown...")
        if tux is not None:
            loop.run_until_complete(shutdown_handler(tux, signal.SIGINT))
    except SystemExit as exc:
        log.info("Shutting down with exit code: %s", exc.code)
        if tux is not None:
            loop.run_until_complete(shutdown_handler(tux, None, exc.code))
        raise
    except Exception as exc:
        log.error("Unexpected exception (%s): ", type(exc))
        console.print_exception(show_locals=True)
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
