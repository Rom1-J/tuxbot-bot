import logging
from pathlib import Path

import appdirs

log = logging.getLogger("tuxbot.core.data_manager")

app_dir = appdirs.AppDirs("Tuxbot-bot")
config_dir = Path(app_dir.user_config_dir)
config_file = config_dir / "config.yaml"


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


def logs_data_path(instance_name: str) -> Path:
    """Return Path for Logs.

    Parameters
    ----------
    instance_name:str

    Returns
    -------
    Path
        Generated path for Logs files.
    """
    return data_path(instance_name) / "Logs"


def cogs_data_path(instance_name: str, cog_name: str = "") -> Path:
    """Return Path for cogs.

    Parameters
    ----------
    instance_name:str
    cog_name:str

    Returns
    -------
    Path
        Generated path for cogs configs.
    """
    return data_path(instance_name) / "cogs" / cog_name
