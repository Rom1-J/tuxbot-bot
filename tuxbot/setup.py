import argparse
import importlib
import logging
import re
import sys
from argparse import Namespace
from pathlib import Path
from typing import NoReturn, Union, List

from rich.prompt import Prompt, IntPrompt
from rich.console import Console
from rich.rule import Rule
from rich.style import Style
from rich.traceback import install

from tuxbot.core.config import set_for
from tuxbot.logging import formatter
from tuxbot.core.data_manager import config_dir, app_dir, cogs_data_path
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

app_config = config.ConfigFile(config_dir / "config.yaml", config.AppConfig)

if not app_config.config.instances:
    instances_list = []
else:
    instances_list = list(app_config.config.instances.keys())


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

    (data_path_input / "logs").mkdir(parents=True, exist_ok=True)

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
            mod_extra = getattr(mod, "extra")

            mod_config = config.ConfigFile(
                str(cogs_data_path(instance, cog_name) / "config.yaml"),
                mod_config_type,
            ).config

            extras = {}

            for key, value in mod_extra.items():
                extras[key] = get_extra(value["description"], value["type"])

            console.log(mod_config)
            console.log(dir(mod_config))
            console.log(mod_config_type)
            set_for(mod_config, **extras)
        else:
            console.print(
                Rule(
                    f"\nFailed to fetch information for `{cog_name}` module",
                    style=Style(color="red"),
                )
            )


def finish_setup(data_dir: Path) -> NoReturn:
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

    instance_config = config.ConfigFile(
        str(data_dir / "config.yaml"), config.Config
    )

    instance_config.config.Core.owners_id = owners_id
    instance_config.config.Core.prefixes = prefixes
    instance_config.config.Core.token = token
    instance_config.config.Core.mentionable = mentionable
    instance_config.config.Core.locale = "en-US"


def basic_setup() -> NoReturn:
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

    instance = config.AppConfig.Instance()
    instance.path = str(data_dir.resolve())
    instance.active = False

    app_config.config.instances[name] = instance

    console.print("\n" * 4)

    finish_setup(data_dir)

    console.print()
    console.print(
        f"Instance successfully created! "
        f"You can now run `tuxbot {name}` to launch this instance now or "
        f"setup the additional configs by running "
        f"`tuxbot-setup {name} --additional-config=all`"
    )


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

    args = parser.parse_args(args)

    return args


def setup() -> NoReturn:
    cli_flags = parse_cli_flags(sys.argv[1:])

    try:
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
