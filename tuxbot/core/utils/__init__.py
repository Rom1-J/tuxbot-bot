"""Set of utils functions and classes."""

import typing

from .colors import Colors
from .emotes import Emotes
from .generators import gen_key as _gen_key
from .generators import shorten as _shorten


class Utils:
    """Set of utils functions and classes."""

    colors: type[Colors] = Colors
    emotes: type[Emotes] = Emotes

    # =========================================================================

    @staticmethod
    async def shorten(text: str, length: int) -> dict[str, str]:
        return await _shorten(text=text, length=length)

    @staticmethod
    def gen_key(
        *args: typing.Unpack[tuple[typing.Any, ...]],
    ) -> str:
        return _gen_key(*args)


utils = Utils()
