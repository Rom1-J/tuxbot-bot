from tuxbot.core.config import set_for_key, search_for

from tuxbot.core import Config

from tuxbot.core.utils.functions.extra import ContextPlus


async def get_blacklist(model, ctx: ContextPlus) -> dict:
    return search_for(model, ctx.author.id, "aliases")


async def blacklist_guild(model, guild_id: int) -> None:
    set_for_key(model, guild_id, Config.Server, blacklisted=True)
