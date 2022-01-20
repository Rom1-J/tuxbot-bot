"""
Set of utils functions and classes
"""

from typing import Type, Callable, Coroutine, Any

from .SetInterval import SetInterval
from .Colors import Colors
from .Generators import gen_key, shorten


class Utils:
    """Set of utils functions and classes"""

    SetInterval: Type[SetInterval] = SetInterval
    Colors: Type[Colors] = Colors
    gen_key: Callable = gen_key
    shorten: Callable[..., Coroutine[Any, Any, Any]] = shorten


utils = Utils()
