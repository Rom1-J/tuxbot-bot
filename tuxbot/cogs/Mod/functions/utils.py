from tuxbot.core.config import set_for_key
from tuxbot.core.config import Config

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus


async def save_lang(bot: Tux, ctx: ContextPlus, lang: str):
    set_for_key(
        bot.config.Servers, ctx.guild.id, Config.Server, locale=lang
    )
