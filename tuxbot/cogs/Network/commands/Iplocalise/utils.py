"""
tuxbot.cogs.Network.functions.Iplocalise.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""

import socket
from typing import Optional, Union

from .exceptions import VersionNotFound


async def get_ip(loop, ip: str, inet: Optional[int]) -> str:
    """Get ip from domain"""

    _inet: Union[socket.AddressFamily, int] = 0  # pylint: disable=no-member

    if inet:
        _inet = socket.AF_INET6 if inet == 6 else socket.AF_INET

    def _get_ip(_ip: str):
        try:
            return socket.getaddrinfo(_ip, None, _inet)[1][4][0]
        except (socket.gaierror, UnicodeError) as e:
            raise VersionNotFound(
                "Unable to collect information on this in the given version"
            ) from e

    return await loop.run_in_executor(None, _get_ip, str(ip))
