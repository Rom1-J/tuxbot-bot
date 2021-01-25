import functools

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
