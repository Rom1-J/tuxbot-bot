import logging
from pathlib import Path
from typing import List

import discord
from colorama import Fore, Style, init
from discord.ext import commands
from . import Config

from .utils.functions.cli import bordered

from . import __version__

log = logging.getLogger("tuxbot")
init()

NAME = r"""
  _____           _           _        _           _   
 |_   _|   ___  _| |__   ___ | |_     | |__   ___ | |_ 
   | || | | \ \/ / '_ \ / _ \| __|____| '_ \ / _ \| __|
   | || |_| |>  <| |_) | (_) | ||_____| |_) | (_) | |_ 
   |_| \__,_/_/\_\_.__/ \___/ \__|    |_.__/ \___/ \__|                                    
"""

l_extensions: List[str] = [
    "jishaku"
]


class Tux(commands.AutoShardedBot):
    def __init__(self, *args, cli_flags=None, bot_dir: Path = Path.cwd(), **kwargs):
        # by default, if the bot shutdown without any intervention,
        # it's a crash
        self.shutdown_code = 1
        self.cli_flags = cli_flags
        self.instance_name = self.cli_flags.instance_name
        self.last_exception = None

        self.config = Config(self.instance_name)

        async def _prefixes(bot, message) -> List[str]:
            prefixes = self.config.get_prefixes(message.guild)

            if self.config('core').get('mentionable'):
                return commands.when_mentioned_or(*prefixes)(bot, message)
            return prefixes

        if "command_prefix" not in kwargs:
            kwargs["command_prefix"] = _prefixes

        if "owner_ids" in kwargs:
            kwargs["owner_ids"] = set(kwargs["owner_ids"])
        else:
            kwargs["owner_ids"] = self.config.owner_ids()

        message_cache_size = 100_000
        kwargs["max_messages"] = message_cache_size
        self.max_messages = message_cache_size

        self.uptime = None
        self.main_dir = bot_dir

        super().__init__(*args, help_command=None, **kwargs)

    async def on_ready(self):
        INFO = {
            'title': "INFO",
            'rows': [
                str(self.user),
                f"Prefixes: {', '.join(self.config('core').get('prefixes'))}",
                f"Language: {self.config('core').get('locale')}",
                f"Tuxbot Version: {__version__}",
                f"Discord.py Version: {discord.__version__}",
                f"Shards: {self.shard_count}",
                f"Servers: {len(self.guilds)}",
                f"Users: {len(self.users)}"
            ]
        }

        COGS = {
            'title': "COGS",
            'rows': []
        }
        for extension in l_extensions:
            COGS['rows'].append(
                f"[{'X' if extension in self.extensions else ' '}] {extension}"
            )

        print(Fore.LIGHTBLUE_EX + NAME)
        print(Style.RESET_ALL)
        print(bordered(INFO, COGS))

        print(f"\n{'=' * 118}\n\n")
