import asyncio
import functools
from typing import Dict

import aiohttp
from discord.ext import commands

from tuxbot.core.utils.functions.extra import ContextPlus


def upper_first(string: str) -> str:
    return "".join(string[0].upper() + string[1:])


def typing(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        context = (
            args[0]
            if isinstance(args[0], (commands.Context, ContextPlus))
            else args[1]
        )

        async with context.typing():
            await func(*args, **kwargs)

    return wrapped


async def shorten(
    session, text: str, length: int, fail: bool = False
) -> tuple[bool, dict]:
    output: Dict[str, str] = {"text": text[:length], "link": ""}

    if len(text) > length:
        output["text"] += "[...]"

        if not fail:
            try:
                async with session.post(
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


def replace_in_dict(value: dict, search: str, replace: str) -> dict:
    clean = {}

    for k, v in value.items():
        if isinstance(v, (str, bytes)):
            v = v.replace(search, replace)  # type: ignore
        elif isinstance(v, list):
            v = replace_in_list(v, search, replace)
        elif isinstance(v, dict):
            v = replace_in_dict(v, search, replace)

        clean[k] = v

    return clean


def replace_in_list(value: list, search: str, replace: str) -> list:
    clean = []

    for v in value:
        if isinstance(v, (str, bytes)):
            v = v.replace(search, replace)  # type: ignore
        elif isinstance(v, list):
            v = replace_in_list(v, search, replace)
        elif isinstance(v, dict):
            v = replace_in_dict(v, search, replace)

        clean.append(v)

    return clean
