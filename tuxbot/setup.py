import json
import logging
import re
import sys
from pathlib import Path
from typing import NoReturn, Union, List, Set

import click
from colorama import Fore, Style, init

from tuxbot.core.data_manager import config_dir, app_dir

init()

try:
    config_dir.mkdir(parents=True, exist_ok=True)
except PermissionError:
    print(f"mkdir: cannot create directory '{config_dir}': Permission denied")
    sys.exit(1)

config_file = config_dir / "config.json"


def load_existing_config() -> dict:
    """Loading and returning configs.

    Returns
    -------
    dict
        a dict containing all configurations.

    """
    if not config_file.exists():
        return {}

    with config_file.open() as fs:
        return json.load(fs)


instances_data = load_existing_config()
if not instances_data:
    instances_list = []
else:
    instances_list = list(instances_data.keys())


def save_config(name: str, data: dict, delete=False) -> NoReturn:
    """save data in config file.

    Parameters
    ----------
    name:str
        name of instance.
    data:dict
        settings for `name` instance.
    delete:bool
        delete or no data.
    """
    _config = load_existing_config()

    if delete and name in _config:
        _config.pop(name)
    else:
        _config[name] = data

    with config_file.open("w") as fs:
        json.dump(_config, fs, indent=4)


def get_name() -> str:
    """Get instance name via input.

    Returns
    -------
    str
        The instance name choose by user.
    """
    name = ""
    while not name:
        print(
            "What name do you want to give this instance?\n"
            "(valid characters: A-Z, a-z, 0-9, _, -)"
        )
        name = input("> ")
        if re.fullmatch(r"[a-zA-Z0-9_\-]*", name) is None:
            print()
            print(
                Fore.RED
                + "ERROR: Invalid characters provided"
                + Style.RESET_ALL
            )
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
    print()

    def make_data_dir(path: Path) -> Union[Path, str]:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError:
            print()
            print(
                Fore.RED
                + f"mkdir: cannot create directory '{path}':"
                  f" Permission denied"
                + Style.RESET_ALL
            )
            path = ""

        return path

    while not data_path_input:
        print(
            "where do you want to save the configurations?\n"
            "Press [enter] to keep the default path"
        )
        print()
        print(f"Default: {data_path}")

        data_path_input = input("> ")

        if data_path_input != '':
            data_path_input = Path(data_path_input)

            try:
                exists = data_path_input.exists()
            except OSError:
                print()
                print(
                    Fore.RED
                    + "Impossible to verify the validity of the path, "
                      "make sure it does not contain any invalid characters."
                    + Style.RESET_ALL
                )
                data_path_input = ""
                exists = False

            if data_path_input and not exists:
                data_path_input = make_data_dir(data_path_input)
        else:
            data_path_input = make_data_dir(data_path)

    print()
    print(
        f"You have chosen {data_path_input} to be your config directory for "
        f"`{instance_name}` instance"
    )

    if not click.confirm("Please confirm", default=True):
        print("Rerun the process to redo this configuration.")
        sys.exit(0)

    (data_path_input / 'core').mkdir(parents=True, exist_ok=True)
    (data_path_input / 'cogs').mkdir(parents=True, exist_ok=True)
    (data_path_input / 'logs').mkdir(parents=True, exist_ok=True)

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
        print(
            "Please enter the bot token\n"
            "(you can find it at https://discord.com/developers/applications)"
        )
        token = input("> ")
        if re.fullmatch(r"([a-zA-Z0-9]{24}\.[a-zA-Z0-9_]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84})", token) is None:
            print(
                Fore.RED
                + "ERROR: Invalid token provided"
                + Style.RESET_ALL
            )
            token = ""
    return token


def get_multiple(question: str, confirmation: str, value_type: type)\
        -> List[Union[str, int]]:
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
    print(question)
    values = [value_type(input('> '))]

    while click.confirm(confirmation, default=False):
        values.append(value_type(input('> ')))

    return values


def additional_config() -> dict:
    """Asking for additional configs in cogs.

    Returns
    -------
    dict:
        Dict with cog name as key and configs as value.
    """
    p = Path(r'tuxbot/cogs').glob('**/additional_config.json')
    datas = {}

    for file in p:
        print()
        cog_name = str(file.parent).split('/')[-1]
        datas[cog_name] = {}

        with file.open('r') as f:
            data = json.load(f)

        print(f"\n==Configuration for `{cog_name}` module==")

        for key, value in data.items():
            print()
            print(value['description'])
            datas[cog_name][key] = input('> ')

    return datas


def finish_setup(data_dir: Path) -> NoReturn:
    """Configs who directly refer to the bot.

    Parameters
    ----------
    data_dir:Path
        Where to save configs.
    """
    print("Now, it's time to finish this setup by giving bot informations\n")

    token = get_token()
    print()
    prefixes = get_multiple(
        "Choice a (or multiple) prefix for the bot",
        "Add another prefix ?",
        str
    )
    mentionable = click.confirm(
        "Does the bot answer if it's mentioned?",
        default=True
    )

    owners_id = get_multiple(
        "Give the owner id of this bot",
        "Add another owner ?",
        int
    )

    cogs_config = additional_config()

    core_file = data_dir / 'core' / 'settings.json'
    core = {
        'token': token,
        'prefixes': prefixes,
        'mentionable': mentionable,
        'owners_id': owners_id,
    }

    with core_file.open("w") as fs:
        json.dump(core, fs, indent=4)

    for cog, data in cogs_config.items():
        data_cog_dir = data_dir / 'cogs' / cog
        data_cog_dir.mkdir(parents=True, exist_ok=True)

        data_cog_file = data_cog_dir / 'settings.json'

        with data_cog_file.open("w") as fs:
            json.dump(data, fs, indent=4)


def basic_setup() -> NoReturn:
    """Configs who refer to instances.

    """
    print("Hi ! it's time for you to give me informations about you instance")
    name = get_name()

    data_dir = get_data_dir(name)

    configs = load_existing_config()
    instance_config = configs[name] if name in instances_list else {}

    instance_config["DATA_PATH"] = str(data_dir.resolve())
    instance_config["IS_RUNNING"] = False

    if name in instances_list:
        print()
        print(
            Fore.RED
            + f"WARNING: An instance named `{name}` already exists "
              f"Continuing will overwrite this instance configs."
            + Style.RESET_ALL
        )
        if not click.confirm("Are you sure you want to continue?",
                             default=False):
            print("Abandon...")
            sys.exit(0)

    save_config(name, instance_config)

    print("\n"*4)

    finish_setup(data_dir)

    print()
    print(
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
            datefmt="%Y-%m-%d %H:%M:%S", style="{"
        )
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        base_logger.addHandler(stdout_handler)

        basic_setup()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    setup()
