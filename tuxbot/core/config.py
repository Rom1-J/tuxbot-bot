"""
Tuxbot core module: config

Contains all config workers
"""
import yaml
from pathlib import Path

cwd = Path().resolve().parent.resolve()
base_path = Path().resolve()
python_base_path = ""

with open(cwd / "data" / "settings" / "development.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

config["paths"] = {
    "cwd": cwd,
    "base": base_path,
    "python_base": python_base_path,
    "cogs": base_path / "cogs",
    "python_cogs": python_base_path + ".cogs",
}
