from tuxbot.core.config import set_for_key, search_for

from tuxbot.core import Config

from tuxbot.core.utils.functions.extra import ContextPlus


async def get_aliases(model, ctx: ContextPlus) -> dict:
    return search_for(model, ctx.author.id, "aliases")


async def save_lang(model, ctx: ContextPlus, lang: str) -> None:
    set_for_key(model, ctx.author.id, Config.User, locale=lang)


async def save_alias(model, ctx: ContextPlus, alias: dict) -> None:
    set_for_key(model, ctx.author.id, Config.User, alias=alias)
