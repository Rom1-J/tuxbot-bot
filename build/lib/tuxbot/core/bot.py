from pathlib import Path

from discord.ext import commands
from . import Config
from . import data_manager


__all__ = ["Tux"]


class Tux(commands.AutoShardedBot):
    def __init__(self, *args, cli_flags=None, bot_dir: Path = Path.cwd(), **kwargs):
        # by default, if the bot shutdown without any intervention,
        # it's a crash
        self.shutdown_code = 1
        self.cli_flags = cli_flags
        self.instance_name = self.cli_flags.instance_name
        self.last_exception = None

        self.config = Config(
            data_manager.get_data_path(self.instance_name)
        )
        self.config.register_global(
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
        self.config.register_guild(
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
        self.config.register_channel(
            ignored=False
        )

        if "owner_ids" in kwargs:
            kwargs["owner_ids"] = set(kwargs["owner_ids"])
        else:
            kwargs["owner_ids"] = self.config.owner_ids()

        message_cache_size = 100_000
        kwargs["max_messages"] = message_cache_size
        self.max_messages = message_cache_size

        self.uptime = None
        self.main_dir = bot_dir

        print(str(self.cli_flags), self.instance_name, self.config, self.owner_ids, self.main_dir)

        exit()

        super().__init__(*args, help_command=None, **kwargs)
