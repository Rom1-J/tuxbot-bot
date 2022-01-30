"""
Set of utils functions and classes
"""

from typing import Type, Callable, Coroutine, Any

from .SetInterval import SetInterval

# noinspection PyPep8Naming
from .Colors import Colors as colors
from .Generators import gen_key, shorten


class Utils:
    """Set of utils functions and classes"""

    SetInterval: Type[SetInterval] = SetInterval
    colors: Type[colors] = colors
    gen_key: Callable = gen_key
    shorten: Callable[..., Coroutine[Any, Any, Any]] = shorten


utils = Utils()
