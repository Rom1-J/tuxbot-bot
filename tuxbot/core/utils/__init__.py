"""
Set of utils functions and classes
"""

import typing

from .Colors import Colors
from .Generators import gen_key as _gen_key
from .Generators import shorten as _shorten


class Utils:
    """Set of utils functions and classes"""

    colors: type[Colors] = Colors
    emotes: list[str] = [chr(0x1F1E6 + i) for i in range(26)]

    # =========================================================================

    @staticmethod
    async def shorten(text: str, length: int) -> dict[str, str]:
        return await _shorten(text=text, length=length)

    @staticmethod
    def gen_key(*args: typing.Any, **kwargs: typing.Any) -> str:
        return _gen_key(*args, **kwargs)


utils = Utils()
