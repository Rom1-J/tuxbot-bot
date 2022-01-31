"""
Set of utils functions and classes
"""

from typing import Any, Callable, Coroutine, Type

# noinspection PyPep8Naming
from .Colors import Colors as colors  # noqa: F401
from .Generators import gen_key, shorten  # noqa: F401


class Utils:
    """Set of utils functions and classes"""

    colors: Type[colors] = colors  # noqa: F811
    gen_key: Callable = gen_key  # noqa: F811
    shorten: Callable[..., Coroutine[Any, Any, Any]] = shorten  # noqa: F811


utils = Utils()
