import logging
from pathlib import Path

import appdirs

log = logging.getLogger("tuxbot.data_manager")

app_dir = appdirs.AppDirs("Tuxbot-bot")
config_dir = Path(app_dir.user_config_dir)
config_file = config_dir / "config.json"


def data_path(instance_name: str) -> Path:
    """Return Path for data configs.

    Parameters
    ----------
    instance_name:str

    Returns
    -------
    Path
        Generated path for data configs.
    """
    return Path(app_dir.user_data_dir) / "data" / instance_name


def core_path(instance_name: str) -> Path:
    """Return Path for core configs.

    Parameters
    ----------
    instance_name:str

    Returns
    -------
    Path
        Generated path for core configs.
    """
    return data_path(instance_name) / "data" / instance_name / "core"


def cogs_data_path(instance_name: str) -> Path:
    """Return Path for cogs configs.

    Parameters
    ----------
    instance_name:str

    Returns
    -------
    Path
        Generated path for cogs configs.
    """
    return data_path(instance_name) / "data" / instance_name / "cogs"


def cog_data_path(instance_name: str, cog_name: str) -> Path:
    """Return Path for chosen configs for cog.

    Parameters
    ----------
    instance_name:str
    cog_name:str

    Returns
    -------
    Path
        Generated path for cog's configs.
    """
    return data_path(instance_name) / "data" / instance_name / "cogs" / cog_name
