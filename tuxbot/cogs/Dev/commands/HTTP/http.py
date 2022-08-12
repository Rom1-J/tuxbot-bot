from .HTTPs import *  # noqa: F403


def http_if_exists(code: int) -> type[HttpCode] | None:  # noqa: F405
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

    if (http := globals().get(f"Http{code}")) and isinstance(
        http(), HttpCode  # noqa: F405
    ):
        return http  # type: ignore

    return None
