import logging

from .base import *  # noqa
from .base import env


# Sentry
# -----------------------------------------------------------------------------
SENTRY_DSN = env.str("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("SENTRY_LOG_LEVEL", logging.INFO)


# Datadog
# -----------------------------------------------------------------------------
STATSD_HOST = env.str("STATSD_HOST", "127.0.0.1")
STATSD_PORT = env.int("STATSD_PORT", 8125)
STATSD_NAMESPACE = env.str("STATSD_NAMESPACE", "tuxbot_metric")

if env.bool("DD_ACTIVE", False):
    from datadog import initialize
    from ddtrace import patch

    initialize(
        statsd_host=STATSD_HOST,
        statsd_port=STATSD_PORT,
        statsd_namespace=STATSD_NAMESPACE,
    )

    patch(
        aioredis=True,
        asyncio=True,
        requests=True,
        asyncpg=True,
        logging=True,
    )
