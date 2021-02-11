import argparse
import importlib
import logging
import os
import re
import sys
import json
from argparse import Namespace
from pathlib import Path
from typing import Union, List
from urllib import request

from rich.prompt import Prompt, IntPrompt
from rich.console import Console
from rich.rule import Rule
from rich.style import Style
from rich.traceback import install

from tuxbot import version_info
from tuxbot.core.config import set_for, set_for_key
from tuxbot.logging import formatter
from tuxbot.core.utils.data_manager import config_dir, app_dir, cogs_data_path
from tuxbot.core import config

console = Console()
install(console=console)

try:
    config_dir.mkdir(parents=True, exist_ok=True)
except PermissionError:
    console.print(
        f"mkdir: cannot create directory '{config_dir}': Permission denied"
    )
    sys.exit(1)

app_config = config.ConfigFile(
    config_dir / "config.yaml", config.AppConfig
).config

if not app_config.Instances:
    instances_list = []
else:
    instances_list = list(app_config.Instances.keys())


def get_name() -> str:
    """Get instance name via input.

    Returns
    -------
    str
        The instance name choose by user.
    """
    name = ""
    while not name:
        name = Prompt.ask(
            "What name do you want to give this instance?\n"
            "[i](valid characters: A-Z, a-z, 0-9, _, -)[/i]\n",
            default="prod",
            console=console,
        )
        if re.fullmatch(r"[a-zA-Z0-9_\-]*", name) is None:
            console.print()
            console.print("[prompt.invalid]ERROR: Invalid characters provided")
            name = ""
    return name


def get_data_dir(instance_name: str) -> Path:
    """Returning data path.

    Parameters
    ----------
    instance_name:str
        Instance name.

    Returns
    -------
    Path
        The data config path corresponding to the instance.

    """
    data_path = Path(app_dir.user_data_dir) / "data" / instance_name
    data_path_input = ""
    console.print()

    def make_data_dir(path: Path) -> Union[Path, str]:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError:
            console.print()
            console.print(
                f"mkdir: cannot create directory '{path}': Permission denied"
            )
            path = ""

        return path

    while not data_path_input:
        data_path_input = Path(
            Prompt.ask(
                "where do you want to save the configurations?",
                default=str(data_path),
                console=console,
            )
        )

        try:
            exists = data_path_input.exists()
        except OSError:
            console.print()
            console.print(
                "[prompt.invalid]"
                "Impossible to verify the validity of the path,"
                " make sure it does not contain any invalid characters."
            )
            data_path_input = ""
            exists = False

        if data_path_input and not exists:
            data_path_input = make_data_dir(data_path_input)

    console.print()
    console.print(
        f"You have chosen {data_path_input} to be your config directory for "
        f"`{instance_name}` instance"
    )

    if (
        Prompt.ask(
            "Please confirm", choices=["y", "n"], default="y", console=console
        )
        != "y"
    ):
        console.print("Rerun the process to redo this configuration.")
        sys.exit(0)

    (data_path_input / "Logs").mkdir(parents=True, exist_ok=True)

    return data_path_input


def get_token() -> str:
    """Get token via input.

    Returns
    -------
    str
        The token choose by user.
    """
    token = ""

    while not token:
        token = Prompt.ask(
            "Please enter the bot token "
            "(you can find it at https://discord.com/developers/applications)",
            console=console,
        )
        if (
            re.fullmatch(
                r"([a-zA-Z0-9]{24}\.[a-zA-Z0-9_]{6}\.[a-zA-Z0-9_\-]{27}"
                r"|mfa\.[a-zA-Z0-9_\-]{84})",
                token,
            )
            is None
        ):
            console.print("[prompt.invalid]ERROR: Invalid token provided")
            token = ""
    return token


def get_ip() -> str:
    """Get ip via input.

    Returns
    -------
    str
        The ip choose by user.
    """
    ip = ""

    # pylint: disable=line-too-long
    ipv4_pattern = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    ipv6_pattern = r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"

    while not ip:
        ip = Prompt.ask(
            "Please the ip of this machine "
            "(you can find it with `curl ifconfig.me`)",
            console=console,
        )
        ipv4 = re.match(ipv4_pattern, ip)
        ipv6 = re.match(ipv6_pattern, ip)

        if not ipv4 and not ipv6:
            console.print("[prompt.invalid]ERROR: Invalid ip provided")
            ip = ""
    return ip


def get_multiple(
    question: str, confirmation: str, value_type: type
) -> List[Union[str, int]]:
    """Give possibility to user to fill multiple value.

    Parameters
    ----------
    question:str
        First question.
    confirmation:str
        Asking text if user want to add another.
    value_type:type
        The type of values inside the list.

    Returns
    -------
    List[Union[str, int]]
        List containing user filled values.
    """
    prompt = IntPrompt if value_type is int else Prompt

    user_input = prompt.ask(question, console=console)

    if not user_input:
        return []

    values = [user_input]

    while (
        Prompt.ask(
            confirmation, choices=["y", "n"], default="n", console=console
        )
        != "n"
    ):
        new = prompt.ask("Other")

        if new not in values:
            values.append(new)
        else:
            console.print(
                f"[prompt.invalid]"
                f"ERROR: `{new}` is already present, [i]ignored[/i]"
            )

    return values


def get_extra(question: str, value_type: type) -> Union[str, int]:
    prompt = IntPrompt if value_type is int else Prompt
    return prompt.ask(question, console=console)


def additional_config(instance: str, cogs: str = "**"):
    """Asking for additional configs in cogs.

    Returns
    -------
    dict:
        Dict with cog name as key and configs as value.
    """
    if cogs is None or "all" in sum(cogs, []):
        cogs = []
    else:
        cogs = sum(cogs, [])

    if len(cogs) == 0:
        paths = Path("tuxbot/cogs").glob("**/config.py")
    else:
        paths = [Path(f"tuxbot/cogs/{cog}/config.py") for cog in cogs]

    for path in paths:
        cog_name = str(path.parent).split("/")[-1]
        if path.exists():
            console.print(Rule(f"\nConfiguration for `{cog_name}` module"))
            mod = importlib.import_module(str(path).replace("/", ".")[:-3])
            mod_config_type = getattr(mod, cog_name.capitalize() + "Config")
            mod_extra = mod.extra

            mod_config = config.ConfigFile(
                str(cogs_data_path(instance, cog_name) / "config.yaml"),
                mod_config_type,
            ).config

            extras = {}

            for key, value in mod_extra.items():
                extras[key] = get_extra(value["description"], value["type"])

            set_for(mod_config, **extras)
        else:
            console.print(
                Rule(
                    f"\nFailed to fetch information for `{cog_name}` module",
                    style=Style(color="red"),
                )
            )


def finish_setup(data_dir: Path) -> None:
    """Configs who directly refer to the bot.

    Parameters
    ----------
    data_dir:Path
        Where to save configs.
    """
    console.print(
        Rule("Now, it's time to finish this setup by giving bot information")
    )
    console.print()

    token = get_token()

    ip = get_ip()

    console.print()
    prefixes = get_multiple(
        "Choice a (or multiple) prefix for the bot",
        "Add another prefix ?",
        str,
    )

    console.print()
    mentionable = (
        Prompt.ask(
            "Does the bot answer if it's mentioned?",
            choices=["y", "n"],
            default="y",
        )
        == "y"
    )

    console.print()
    owners_id = get_multiple(
        "Give the owner id of this bot", "Add another owner ?", int
    )

    console.print("\n" * 4)
    console.print(Rule("\nAnd to finish, the configuration for PostgreSQL"))
    console.print()

    database = {
        "username": Prompt.ask(
            "Please enter the username for PostgreSQL",
            console=console,
        ),
        "password": Prompt.ask(
            "Please enter the password for PostgreSQL",
            console=console,
        ),
        "domain": Prompt.ask(
            "Please enter the domain for PostgreSQL",
            console=console,
            default="localhost",
        ),
        "port": IntPrompt.ask(
            "Please enter the port for PostgreSQL",
            console=console,
            default="5432",
        ),
        "db_name": Prompt.ask(
            "Please enter the database name for PostgreSQL", console=console
        ),
    }

    instance_config = config.ConfigFile(
        str(data_dir / "config.yaml"), config.Config
    )

    instance_config.config.Core.owners_id = owners_id
    instance_config.config.Core.prefixes = prefixes
    instance_config.config.Core.token = token
    instance_config.config.Core.ip = ip
    instance_config.config.Core.mentionable = mentionable
    instance_config.config.Core.locale = "en-US"

    instance_config.config.Core.Database.username = database["username"]
    instance_config.config.Core.Database.password = database["password"]
    instance_config.config.Core.Database.domain = database["domain"]
    instance_config.config.Core.Database.port = database["port"]
    instance_config.config.Core.Database.db_name = database["db_name"]


def basic_setup() -> None:
    """Configs who refer to instances."""
    console.print(
        Rule(
            "Hi ! it's time for you to give me information about you instance"
        )
    )
    console.print()
    name = get_name()

    data_dir = get_data_dir(name)

    if name in instances_list:
        console.print()
        console.print(
            f"WARNING: An instance named `{name}` already exists "
            f"Continuing will overwrite this instance configs.",
            style="red",
        )
        if (
            Prompt.ask(
                "Are you sure you want to continue?",
                choices=["y", "n"],
                default="n",
            )
            == "n"
        ):
            console.print("Abandon...")
            sys.exit(0)

    set_for_key(
        app_config.Instances,
        name,
        config.AppConfig.Instance,
        path=str(data_dir.resolve()),
        active=False,
    )

    console.print("\n" * 4)

    finish_setup(data_dir)

    console.print()
    console.print(
        f"Instance successfully created! "
        f"You can now run `tuxbot {name}` to launch this instance now or "
        f"setup the additional configs by running "
        f"`tuxbot-setup {name} --additional-config=all`"
    )


def update() -> None:
    response = json.load(
        request.urlopen(
            "https://api.github.com/repos/Rom1-J/tuxbot-bot/commits/master"
        )
    )  # skipcq:  BAN-B310

    if response.get("sha")[:6] == version_info.build:
        print(
            "Nothing to update, you can run `tuxbot [instance_name]` "
            "to start the bot"
        )
    else:
        print(f"Updating to {response.get('sha')[:6]}...")

        os.popen("/usr/bin/git pull")

        print("Done!")


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
        description="Tuxbot Setup - OpenSource bot",
        usage="tuxbot-setup [instance] [arguments]",
    )
    parser.add_argument(
        "instance_name",
        nargs="?",
        help="Name of the bot instance to edit.",
    )
    parser.add_argument(
        "-a",
        "--additional-config",
        action="append",
        nargs="+",
        help="Execute setup to additional configs",
    )
    parser.add_argument(
        "-U",
        "--update",
        action="store_true",
        help="Check for update",
    )

    args = parser.parse_args(args)

    return args


def setup() -> None:
    cli_flags = parse_cli_flags(sys.argv[1:])

    try:
        if cli_flags.update:
            update()
            sys.exit()

        # Create a new instance.
        level = logging.DEBUG
        base_logger = logging.getLogger("tuxbot")
        base_logger.setLevel(level)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        base_logger.addHandler(stdout_handler)

        if cli_flags.additional_config and not cli_flags.instance_name:
            console.print(
                "[red]No instance to modify provided ! "
                "You can use 'tuxbot -L' to list all available instances"
            )
        elif cli_flags.instance_name:
            additional_config(
                cli_flags.instance_name, cli_flags.additional_config
            )
        else:
            console.clear()
            basic_setup()
    except KeyboardInterrupt:
        console.print("Exiting...")
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    setup()
