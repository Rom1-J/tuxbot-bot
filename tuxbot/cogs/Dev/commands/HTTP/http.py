from .HTTPs import *  # noqa: F403


def http_if_exists(code: int) -> HttpCode | None:  # noqa: F405
    """
    Check if HTTP class for this code exists,
    if it does, return class instance.

    Parameters
    ----------
    code: int
        HTTP code

    Returns
    -------
    Optional[HttpCode]
    """
    if http := globals().get(f"Http{code}"):
        return http

    return None
