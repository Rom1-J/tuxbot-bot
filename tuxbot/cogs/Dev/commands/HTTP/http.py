# pylint: disable=unused-wildcard-import, wildcard-import
from typing import Optional

from .HTTPs.OneXX import *
from .HTTPs.TwoXX import *
from .HTTPs.ThreeXX import *
from .HTTPs.FourXX import *
from .HTTPs.FiveXX import *


def http_if_exists(code: int) -> Optional[HttpCode]:
    """Check if HTTP class for this code exists,
    if it does, return class instance.

    Parameters
    ----------
    code: int
        HTTP code

    Returns
    -------

    """
    # pylint: disable=superfluous-parens
    if (http := f"Http{code}") in globals():
        return globals()[http]

    return None
