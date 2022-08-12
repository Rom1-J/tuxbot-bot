"""
tuxbot.cogs.Network.functions.providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of providers for iplocalise
"""
from .HostnameProvider import HostnameProvider
from .IPGeolocationProvider import IPGeolocationProvider
from .IPInfoProvider import IPInfoProvider
from .IPWhoisProvider import IPWhoisProvider
from .MapProvider import MapProvider
from .OpenCageDataProvider import OpenCageDataProvider


__all__ = (
    "HostnameProvider",
    "IPGeolocationProvider",
    "IPInfoProvider",
    "IPWhoisProvider",
    "MapProvider",
    "OpenCageDataProvider",
)
