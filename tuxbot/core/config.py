"""
Tuxbot core module: config

Contains all config workers
"""

from pathlib import Path
import yaml

cwd = Path().resolve().parent.resolve()
base_path = Path().resolve()
python_base_path = ""

config_path = cwd / "data" / "settings" / "development.yaml"

with open(str(config_path), encoding="UTF-8") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

config["paths"] = {
    "cwd": cwd,
    "base": base_path,
    "python_base": python_base_path,
    "cogs": base_path / "cogs",
    "python_cogs": python_base_path + ".cogs",
}

config["urls"] = {
    "wiki": "https://tuxbot.gnous.eu/wiki",
    "site": "https://tuxbot.gnous.eu",
    "discord": "https://discord.gg/QXmESeghBP",
}
