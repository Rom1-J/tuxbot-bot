"""
Tuxbot core module: config

Contains all config workers
"""
import yaml
from pathlib import Path

base_path = "."

with open(Path().resolve().parent.resolve() / "data" / "settings" / "config.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

config["sentry"] = {
    "dsn": "https://758fc55570d540f5b404f7c01a757823@o511839.ingest.sentry.io/6136538"
}

config["paths"] = {
    "base": base_path,
    "commands": base_path + "commands",
    "controllers": base_path + "controllers",
    "events": base_path + "events",
}
