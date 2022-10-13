import logging
from pathlib import Path

import environ


ROOT_DIR = Path(__file__).resolve(strict=True).parent
APPS_DIR = ROOT_DIR / "tuxbot"

env = environ.Env()


# GENERAL
# -----------------------------------------------------------------------------
LOG_LEVEL = env.int("TUXBOT_LOG_LEVEL", logging.INFO)
CLUSTER_COUNT = env.int("TUXBOT_CLUSTER_COUNT", 1)
SHARDING_STRATEGY = env.str("TUXBOT_SHARDING_STRATEGY", "shard")
FIRST_SHARD_OVERRIDE = env.int("TUXBOT_FIRST_SHARD_ID", 0)
LAST_SHARD_OVERRIDE = env.int("TUXBOT_LAST_SHARD_ID", 0)
SHARD_COUNT_OVERRIDE = env.int("TUXBOT_SHARD_COUNT", 1)
CLUSTER_IDS = env.int("TUXBOT_CLUSTER_ID", 0)
SHARD_IDS = env.int("TUXBOT_SHARD_ID", 1)


# CLIENT
# -----------------------------------------------------------------------------
CLIENT = {
    "id": env.int("TUXBOT_CLIENT_ID"),
    "token": env.int("TUXBOT_CLIENT_TOKEN"),
    "game": env.int("TUXBOT_CLIENT_GAME"),
    "disable_everyone": env.bool("TUXBOT_CLIENT_DISABLE_EVERYONE", True),
    "disable_help": env.bool("TUXBOT_CLIENT_DISABLE_HELP", False),
    "disabled_events": env.list("TUXBOT_CLIENT_DISABLED_EVENTS", []),
    "max_cached_messages": env.int("TUXBOT_CLIENT_MAX_CACHED_MESSAGES", 1_000),
    "owners_id": env.list("TUXBOT_CLIENT_OWNERS_ID"),
}


# DATABASES
# -----------------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://localhost/tuxbot",
    ),
}

REDIS = {"default": env.str("REDIS_URL")}


# COGS
# -----------------------------------------------------------------------------
COGS = [
    "jishaku",
    "tuxbot.cogs.Admin",
]

INSTALLED_COGS = COGS + env.list("TUXBOT_LOADED_COGS", [])


# LOGGING
# -----------------------------------------------------------------------------
WEBHOOKS = {
    "shard": env.str("TUXBOT_WEBHOOK_SHARD", ""),
    "error": env.str("TUXBOT_WEBHOOK_ERROR", ""),
    "cluster": env.str("TUXBOT_WEBHOOK_CLUSTER", ""),
}
