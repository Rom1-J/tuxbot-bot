import logging
import typing
from distutils.dir_util import copy_tree
from pathlib import Path

import environ
import yaml
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
logging.getLogger("environ").setLevel(logging.INFO)
env = environ.Env()


ROOT = Path().resolve()
DATA_PATH = ROOT / "data"
SETTINGS_PATH = DATA_PATH / "settings"

ENV_MIGRATION: dict[str, str] = {
    "development": ".local",
    "production": ".production",
}


KEY_MIGRATION: dict[str, dict[str, str]] = {
    ".bot": {
        # Tuxbot
        "TUXBOT_LOG_LEVEL": "log_level",
        "TUXBOT_CLUSTER_COUNT": "cluster_count",
        "TUXBOT_CLUSTER_ID": "cluster_ids",
        "TUXBOT_SHARD_COUNT": "shard_count_override",
        "TUXBOT_SHARD_ID": "shard_ids",
        "TUXBOT_SHARDING_STRATEGY": "sharding_strategy",
        "TUXBOT_FIRST_SHARD_ID": "first_shard_override",
        "TUXBOT_LAST_SHARD_ID": "last_shard_override",
        # Client
        "TUXBOT_CLIENT_ID": "client.id",
        "TUXBOT_CLIENT_TOKEN": "client.token",
        "TUXBOT_CLIENT_GAME": "client.game",
        "TUXBOT_CLIENT_DISABLE_EVERYONE": "client.disable_everyone",
        "TUXBOT_CLIENT_DISABLE_HELP": "disable_help",
        "TUXBOT_CLIENT_DISABLED_EVENTS": "disable_events",
        "TUXBOT_CLIENT_MAX_CACHED_MESSAGES": "client.max_cached_messages",
        "TUXBOT_CLIENT_OWNERS_ID": "client.owners_id",
        "TUXBOT_CLIENT_PREFIXES": "prefixes",
        # Redis
        "REDIS_URL": "custom:redis_converter(config)",
        # Logging
        "TUXBOT_WEBHOOK_SHARD": "shard_webhook",
        "TUXBOT_WEBHOOK_ERROR": "error_webhook",
        "TUXBOT_WEBHOOK_CLUSTER": "cluster.webhook_url",
        "SENTRY_DSN": "sentry.dsn",
        "SENTRY_LOG_LEVEL": "log_level",
        "DD_ACTIVE": "bool(False)",
        "STATSD_HOST": "str('127.0.0.1')",
        "STATSD_PORT": "int(8125)",
        "STATSD_NAMESPACE": "str('tuxbot_metric')",
        # Cogs
        "TUXBOT_LOADED_COGS": "modules",
    },
    ".cogs": {
        # Math
        "COGS_WOLFRAMALPHA_KEY": "Math.wolframalpha_key",
        # Network
        "COGS_IPINFO_KEY": "Network.ipinfo_key",
        "COGS_GEOAPIFY_KEY": "Network.geoapify_key",
        "COGS_IPGEOLOCATION_KEY": "Network.ipgeolocation_key",
        "COGS_OPENCAGEDATA_KEY": "Network.opencagedata_key",
        "COGS_PEERINGDB_KEY": "str()",
    },
    ".postgres": {
        # PostgreSQL
        "POSTGRES_HOST": "custom:postgres_converter(config, 'host')",
        "POSTGRES_PORT": "custom:postgres_converter(config, 'port')",
        "POSTGRES_DB": "custom:postgres_converter(config, 'db')",
        "POSTGRES_USER": "custom:postgres_converter(config, 'user')",
        "POSTGRES_PASSWORD": "custom:postgres_converter(config, 'password')",
    },
}


def copy_envs() -> None:
    log.info("Copying '.envs.example' to '.envs'")
    copy_tree(str(ROOT / ".envs.example"), str(ROOT / ".envs"))


def get_old_conf(env: str) -> yaml.Loader:
    log.info("Retrieving old configuration for '%s'" % env)

    with open(str(SETTINGS_PATH / f"{env}.yaml"), encoding="UTF-8") as f:
        return yaml.load(  # type: ignore[no-any-return]
            f, Loader=yaml.SafeLoader
        )


def postgres_converter(config: typing.Any, field: str) -> str:
    postgres_dsn = env.db(default=config["postgres"]["dsn"])

    match field:
        case "host":
            return postgres_dsn["HOST"]  # type: ignore[no-any-return]
        case "port":
            return postgres_dsn["PORT"]  # type: ignore[no-any-return]
        case "db":
            return postgres_dsn["NAME"]  # type: ignore[no-any-return]
        case "user":
            return postgres_dsn["USER"]  # type: ignore[no-any-return]
        case "password":
            return postgres_dsn["PASSWORD"]  # type: ignore[no-any-return]

    return config["postgres"]["dsn"]  # type: ignore[no-any-return]


def redis_converter(config: typing.Any) -> str:
    return f"redis://{config['redis']['host']}:{config['redis']['port']}" "/0"


def custom_manager(config: yaml.Loader, payload: str) -> typing.Any:
    return eval(payload)


def migrate(config: yaml.Loader, output: str) -> None:
    custom_keys = {
        "custom": lambda x: custom_manager(config, x),
        "str": lambda x: str(eval(x)),
        "int": lambda x: int(eval(x)),
        "bool": lambda x: bool(eval(x)),
    }

    for file, values in KEY_MIGRATION.items():
        with open(f"{output}/{file}", "r+") as f:
            content = f.read()

            for key, value in values.items():
                if len(s := value.split(":")) > 1:
                    func, arg = s
                    new_value = custom_keys[func](
                        arg
                    )  # type: ignore[no-untyped-call]
                elif (
                    len(s := value.split("(")) > 1
                    and s[0] in custom_keys.keys()
                ):
                    new_value = custom_keys[s[0]](
                        value
                    )  # type: ignore[no-untyped-call]
                else:
                    recursion = config

                    for field in value.split("."):
                        recursion = recursion[field]  # type: ignore[index]

                    new_value = recursion

                content = content.replace(f"{key}=", f'{key}="{new_value}"')

            f.seek(0)
            f.write(content)


def main() -> None:
    if not (ROOT / ".envs").exists():
        copy_envs()
    else:
        log.info("'.envs' already exists, skipping creation")

    if not DATA_PATH.resolve():
        log.error("'data' directory not found, exiting...")
        return

    if not SETTINGS_PATH.resolve():
        log.error("'settings' directory not found, exiting...")
        return

    for old_env, new_env in ENV_MIGRATION.items():
        config = get_old_conf(old_env)

        migrate(config, f".envs/{new_env}")


if __name__ == "__main__":
    main()
