import json
import logging
import re
import sys
from pathlib import Path
from typing import NoReturn, Union, List

from rich.prompt import Prompt, IntPrompt
from rich.console import Console
from rich.rule import Rule
from rich.traceback import install

from tuxbot.core.data_manager import config_dir, app_dir
from tuxbot.core import config

console = Console()
console.clear()
install(console=console)

try:
    config_dir.mkdir(parents=True, exist_ok=True)
except PermissionError:
    console.print(f"mkdir: cannot create directory '{config_dir}': Permission denied")
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
            console=console
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
                console=console
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

    if Prompt.ask(
            "Please confirm",
            choices=["y", "n"], default="y",
            console=console
    ) != "y":
        console.print("Rerun the process to redo this configuration.")
        sys.exit(0)

    (data_path_input / "core").mkdir(parents=True, exist_ok=True)
    (data_path_input / "cogs").mkdir(parents=True, exist_ok=True)
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
            console=console
        )
        if re.fullmatch(
                r"([a-zA-Z0-9]{24}\.[a-zA-Z0-9_]{6}\.[a-zA-Z0-9_\-]{27}"
                r"|mfa\.[a-zA-Z0-9_\-]{84})",
                token) \
                is None:
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

    while Prompt.ask(
            confirmation,
            choices=["y", "n"], default="y",
            console=console
    ) != "n":
        new = prompt.ask("Other")

        if new not in values:
            values.append(new)
        else:
            console.print(
                f"[prompt.invalid]"
                f"ERROR: `{new}` is already present, [i]ignored[/i]"
            )

    return values


def additional_config() -> dict:
    """Asking for additional configs in cogs.

    Returns
    -------
    dict:
        Dict with cog name as key and configs as value.
    """
    p = Path("tuxbot/cogs").glob("**/config.py")
    data = {}

    for file in p:
        console.print("\n" * 4)
        cog_name = str(file.parent).split("/")[-1]
        data[cog_name] = {}

        with file.open("r") as f:
            data = json.load(f)

        console.print(Rule(f"\nConfiguration for `{cog_name}` module"))

        for key, value in data.items():
            console.print()
            data[cog_name][key] = Prompt.ask(value["description"])

    return data


def finish_setup(data_dir: Path) -> NoReturn:
    """Configs who directly refer to the bot.

    Parameters
    ----------
    data_dir:Path
        Where to save configs.
    """
    console.print(
        Rule(
            "Now, it's time to finish this setup by giving bot information"
        )
    )
    console.print()

    token = get_token()

    console.print()
    prefixes = get_multiple(
        "Choice a (or multiple) prefix for the bot", "Add another prefix ?",
        str
    )

    console.print()
    mentionable = Prompt.ask(
        "Does the bot answer if it's mentioned?",
        choices=["y", "n"],
        default="y"
    ) == "y"

    console.print()
    owners_id = get_multiple(
        "Give the owner id of this bot", "Add another owner ?", int
    )

    # cogs_config = additional_config()

    instance_config = config.ConfigFile(
        str(data_dir / "config.yaml"), config.Config
    )

    instance_config.config.Core.owners_id = owners_id
    instance_config.config.Core.prefixes = prefixes
    instance_config.config.Core.token = token
    instance_config.config.Core.mentionable = mentionable
    instance_config.config.Core.locale = "en-US"


def basic_setup() -> NoReturn:
    """Configs who refer to instances.

    """
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
            f"Continuing will overwrite this instance configs.", style="red"
        )
        if Prompt.ask(
                "Are you sure you want to continue?",
                choices=["y", "n"], default="n"
        ) == "n":
            console.print("Abandon...")
            sys.exit(0)

    instance = config.Instance()
    instance.path = str(data_dir.resolve())
    instance.active = False

    app_config.config.instances[name] = instance

    console.print("\n" * 4)

    finish_setup(data_dir)

    console.print()
    console.print(
        f"Instance successfully created! "
        f"You can now run `tuxbot {name}` to launch this instance"
    )


def setup() -> NoReturn:
    try:
        """Create a new instance."""
        level = logging.DEBUG
        base_logger = logging.getLogger("tuxbot")
        base_logger.setLevel(level)
        formatter = logging.Formatter(
            "[{asctime}] [{levelname}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        base_logger.addHandler(stdout_handler)

        basic_setup()
    except KeyboardInterrupt:
        console.print("Exiting...")
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    setup()
