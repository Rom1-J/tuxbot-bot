"""
tuxbot.cogs.Network.functions.providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Set of providers for iplocalise
"""
from .hostname_provider import HostnameProvider
from .ipgeolocation_provider import IPGeolocationProvider
from .ipinfo_provider import IPInfoProvider
from .ipwhois_provider import IPWhoisProvider
from .map_provider import MapProvider
from .opencagedata_provider import OpenCageDataProvider


__all__ = (
    "HostnameProvider",
    "IPGeolocationProvider",
    "IPInfoProvider",
    "IPWhoisProvider",
    "MapProvider",
    "OpenCageDataProvider",
)
