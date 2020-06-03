from pathlib import Path

import appdirs

app_dir = appdirs.AppDirs("Tuxbot-bot")
config_dir = Path(app_dir.user_config_dir)
config_file = config_dir / "config.json"


def get_data_path(instance_name: str) -> Path:
    return Path(app_dir.user_data_dir) / "data" / instance_name


def get_core_path(instance_name: str) -> Path:
    data_path = get_data_path(instance_name)
    return data_path / "data" / instance_name / "core"


def get_cogs_path(instance_name: str) -> Path:
    data_path = get_data_path(instance_name)
    return data_path / "data" / instance_name / "cogs"


def get_cog_path(instance_name: str, cog_name: str) -> Path:
    data_path = get_data_path(instance_name)
    return data_path / "data" / instance_name / "cogs" / cog_name
