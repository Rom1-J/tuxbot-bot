"""
Useful generators
"""
import inspect


def gen_key(*args, **kwargs) -> str:
    """Generate key from args and kwargs used to be set as key name for redis

    Parameters
    ----------
    args: Tuple[Any]
    kwargs Dict[str, Any]

    Returns
    -------
    str
    """

    frame = inspect.stack()[1]
    file = "/tuxbot/" + frame.filename.split("/tuxbot/")[-1]

    base_key = f"{file}>{frame.function}"
    params = ""

    if args:
        params = ",".join([repr(arg) for arg in args])

    if kwargs:
        params += ",".join([f"{k}={repr(v)}" for k, v in kwargs.items()])

    return f"{base_key}({params})"
