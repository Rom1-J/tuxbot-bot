import logging
from discord.ext import commands
from structured_config import ConfigFile

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.data_manager import cogs_data_path
from .config import HelpConfig
from .functions.utils import HelpCommand

log = logging.getLogger("tuxbot.cogs.Help")
_ = Translator("Help", __file__)


class Help(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

        self.__config: HelpConfig = ConfigFile(
            str(cogs_data_path("Help") / "config.yaml"),
            HelpConfig,
        ).config

        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand(self.__config)
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command

    # =========================================================================
    # =========================================================================

    # =========================================================================
