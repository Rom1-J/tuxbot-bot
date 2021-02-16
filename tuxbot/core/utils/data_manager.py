import logging
from pathlib import Path
import os

log = logging.getLogger("tuxbot.core.data_manager")

core_path = Path(os.getcwd())

data_path = core_path / "data"
config_path = data_path / "settings"
config_file = config_path / "config.yaml"


def logs_data_path() -> Path:
    """Return Path for Logs.

    Returns
    -------
    Path
        Generated path for Logs files.
    """
    return data_path / "logs"


def cogs_data_path(cog_name: str = "") -> Path:
    """Return Path for cogs.

    Parameters
    ----------
    cog_name:str

    Returns
    -------
    Path
        Generated path for cogs configs.
    """
    return data_path / "settings" / "cogs" / cog_name
