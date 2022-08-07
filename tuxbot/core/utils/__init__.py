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
    gen_key: typing.Callable[..., str] = _gen_key
    shorten: typing.Callable[
        ..., typing.Coroutine[typing.Any, typing.Any, typing.Any]
    ] = _shorten
    emotes: list[str] = [chr(0x1F1E6 + i) for i in range(26)]


utils = Utils()
