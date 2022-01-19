"""
tuxbot.cogs.Network.functions.Peeringdb.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""

from typing import Union, NoReturn

from tuxbot.cogs.Network.commands.Peeringdb.exceptions import InvalidAsn


def check_asn_or_raise(asn: str) -> Union[bool, NoReturn]:
    """Validate asn format"""

    if asn.isdigit() and int(asn) < 4_294_967_295:
        return True

    raise InvalidAsn("Invalid ASN provided")
