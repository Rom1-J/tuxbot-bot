from .base import *  # noqa: F403
from .base import env


# StatsD
# -----------------------------------------------------------------------------
STATSD_HOST = env.str("STATSD_HOST", "127.0.0.1")
STATSD_PORT = env.int("STATSD_PORT", 8125)
STATSD_NAMESPACE = env.str("STATSD_NAMESPACE", "tuxbot_metric")


# Cogs
# -----------------------------------------------------------------------------
# Math
WOLFRAMALPHA_KEY = env.str("COGS_WOLFRAMALPHA_KEY")

# Network
IPINFO_KEY = env.str("COGS_IPINFO_KEY")
GEOAPIFY_KEY = env.str("COGS_GEOAPIFY_KEY")
IPGEOLOCATION_KEY = env.str("COGS_IPGEOLOCATION_KEY")
OPENCAGEDATA_KEY = env.str("COGS_OPENCAGEDATA_KEY")
PEERINGDB_KEY = env.str("COGS_PEERINGDB_KEY")
