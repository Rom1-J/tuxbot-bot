from pathlib import Path

from discord.ext import commands
from . import Config


__all__ = ["Tux"]


class Tux(commands.AutoShardedBot):
    def __init__(self, *args, bot_dir: Path, **kwargs):
        self._config = Config.register_core(
            identifier=None,
            mentionnable=False
        )
        self._config.register_global(
            token=None,
            prefix=[],
            owner=None,
            whitelist=[],
            blacklist=[],
            locale="en-US",
            embeds=True,
            color=0x6E83D1,
            description="Tuxbot !",
            disabled_commands=[]
        )
        self._config.register_guild(
            prefix=[],
            whitelist=[],
            blacklist=[],
            locale="en-US",
            admin_role=[],
            mod_role=[],
            embeds=None,
            ignored=False,
            disabled_commands=[]
        )
        self._config.register_channel(
            ignored=False
        )