import logging
from discord.ext import commands
from youtrack.connection import Connection as YouTrack
from structured_config import ConfigFile

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.data_manager import cogs_data_path
from .config import DevConfig
from ...core.utils import checks
from ...core.utils.functions.extra import group_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.dev")
_ = Translator("Dev", __file__)


class Dev(commands.Cog, name="Dev"):
    yt: YouTrack  # pylint: disable=invalid-name

    def __init__(self, bot: Tux):
        self.bot = bot
        self.config: DevConfig = ConfigFile(
            str(
                cogs_data_path(self.bot.instance_name, "dev") / "config.yaml"
            ),
            DevConfig,
        ).config

        # pylint: disable=invalid-name
        self.yt = YouTrack(
            self.config.url.rstrip('/') + '/youtrack/',
            login=self.config.login,
            password=self.config.password
        )

    @group_extra(name="issue", aliases=["issues"], deletable=True)
    @checks.is_owner()
    async def _issue(self, ctx: ContextPlus):
        """Manage bot issues."""

    @_issue.command(name="list", aliases=["liste", "all", "view"])
    async def _lang_list(self, ctx: ContextPlus):
        pass
