from pathlib import Path

from discord.ext import commands
from . import Config


__all__ = ["Tux"]


class Tux(commands.AutoShardedBot):
    def __init__(self, *args, cli_flags=None, bot_dir: Path = Path.cwd(), **kwargs):
        # by default, if the bot shutdown without any intervention,
        # it's a crash
        self._shutdown_mode = 1
        self._cli_flags = cli_flags
        self._last_exception = None

        self._config = Config.register_core(
            identifier=self._cli_flags.instance_name
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

        if "owner_ids" in kwargs:
            kwargs["owner_ids"] = set(kwargs["owner_ids"])
        else:
            kwargs["owner_ids"] = self._config.owner_ids()

        message_cache_size = 100_000
        kwargs["max_messages"] = message_cache_size
        self._max_messages = message_cache_size

        self._uptime = None
        self._main_dir = bot_dir

        super().__init__(*args, help_command=None, **kwargs)
