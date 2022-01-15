import logging
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator

log = logging.getLogger("tuxbot.cogs.Stats")
_ = Translator("Stats", __file__)


class Stats(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    # =========================================================================
    # =========================================================================
