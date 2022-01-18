"""
tuxbot.cogs.Network.functions.Peeringdb.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""
from typing import Union, NoReturn


def check_asn_or_raise(asn: str) -> Union[bool, NoReturn]:
    if asn.isdigit() and int(asn) < 4_294_967_295:
        return True

    raise InvalidAsn("Invalid ASN provided")