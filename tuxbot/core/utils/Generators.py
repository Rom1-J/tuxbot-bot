"""
Useful generators
"""
import asyncio
import inspect
from typing import Tuple, Dict

import aiohttp


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


async def shorten(
    text: str, length: int, fail: bool = False
) -> Tuple[bool, dict]:
    """Return either paste url if text is too long,
    or given text if correct size

    Parameters
    ----------
    text: str
        Text to shorten
    length: int
        Max length
    fail: bool
        True if failed to send to paste link

    Returns
    -------
    Dict[str, str]
        trunked text and link if available
    """
    output: Dict[str, str] = {"text": text[:length], "link": ""}

    if len(text) > length:
        output["text"] += "[...]"

        if not fail:
            try:
                async with aiohttp.ClientSession() as cs, cs.post(
                    "https://paste.ramle.be/documents",
                    data=text.encode(),
                    timeout=aiohttp.ClientTimeout(total=0.300),
                ) as r:
                    output[
                        "link"
                    ] = f"https://paste.ramle.be/{(await r.json())['key']}"
            except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
                fail = True

    return fail, output
