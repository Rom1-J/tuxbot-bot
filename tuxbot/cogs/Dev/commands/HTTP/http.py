# pylint: disable=unused-wildcard-import, wildcard-import
from typing import Optional, Type

from .HTTPs.FiveXX import *  # noqa: F403
from .HTTPs.FourXX import *  # noqa: F403
from .HTTPs.OneXX import *  # noqa: F403
from .HTTPs.ThreeXX import *  # noqa: F403
from .HTTPs.TwoXX import *  # noqa: F403


def http_if_exists(code: int) -> Optional[Type[HttpCode]]:  # noqa: F405
    """Check if HTTP class for this code exists,
    if it does, return class instance.

    Parameters
    ----------
    code: int
        HTTP code

    Returns
    -------
    Optional[Type[HttpCode]]
    """
    # pylint: disable=superfluous-parens
    if (http := f"Http{code}") in globals():
        return globals()[http]

    return None
