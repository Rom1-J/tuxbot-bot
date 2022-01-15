# pylint: disable=unused-wildcard-import, wildcard-import
from .HTTPs.OneXX import *
from .HTTPs.TwoXX import *
from .HTTPs.ThreeXX import *
from .HTTPs.FourXX import *
from .HTTPs.FiveXX import *


def http_if_exists(code: int):
    # pylint: disable=superfluous-parens
    if (http := f"Http{code}") in globals():
        return globals()[http]

    return None
