"""
Useful generators
"""
import asyncio
import inspect
import textwrap
import typing

import aiohttp


def gen_key(*args: typing.Any, **kwargs: typing.Any) -> str:
    frame = inspect.stack()[1]
    file = "/tuxbot/" + frame.filename.split("/tuxbot/")[-1]

    base_key = f"{file}>{frame.function}"
    params = ""

    if args:
        params = ",".join([repr(arg) for arg in args])

    if kwargs:
        params += ",".join([f"{k}={repr(v)}" for k, v in kwargs.items()])

    return f"{base_key}({params})"


async def shorten(text: str, length: int) -> dict[str, str]:
    output: dict[str, str] = {
        "text": textwrap.shorten(text, length),
        "link": "",
    }

    if output["text"] != text:
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
            pass

    return output
