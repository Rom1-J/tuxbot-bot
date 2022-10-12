import logging

from .base import *  # noqa
from .base import env


# Sentry
# -----------------------------------------------------------------------------
SENTRY_DSN = env.str("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("SENTRY_LOG_LEVEL", logging.INFO)


# Datadog
# -----------------------------------------------------------------------------
STATSD_HOST = env.str("STATSD_HOST", "")

if env.bool("DD_ACTIVE", False):
    from datadog import initialize
    from ddtrace import patch

    initialize(
        statsd_host=STATSD_HOST,
        statsd_port=8125,
        statsd_namespace="tuxbot_metric",
    )

    patch(
        aioredis=True,
        asyncio=True,
        requests=True,
        asyncpg=True,
        logging=True,
    )
