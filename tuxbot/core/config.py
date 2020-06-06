import asyncio
import json
import logging
from typing import List, Dict, Union, Any

import discord

from tuxbot.core.data_manager import data_path

__all__ = ["Config"]

log = logging.getLogger("tuxbot.core.config")


class Config:
    def __init__(self, cog_instance: str = None):
        self._cog_instance = cog_instance

        self.lock = asyncio.Lock()
        self.loop = asyncio.get_event_loop()

        self._settings_file = None
        self._datas = {}

    def __getitem__(self, item) -> Dict:
        path = data_path(self._cog_instance)

        if item != "core":
            path = path / "cogs" / item
        else:
            path /= "core"

        settings_file = path / "settings.json"

        if not settings_file.exists():
            raise FileNotFoundError(
                f"Unable to find settings file " f"'{settings_file}'"
            )
        else:
            with settings_file.open("r") as f:
                return json.load(f)

    def __call__(self, item):
        return self.__getitem__(item)

    def owners_id(self) -> List[int]:
        """Simply return the owners id saved in config file.

        Returns
        -------
        str
            Owners id.
        """
        return self.__getitem__("core").get("owners_id")

    def token(self) -> str:
        """Simply return the bot token saved in config file.

        Returns
        -------
        str
            Bot token.
        """
        return self.__getitem__("core").get("token")

    def get_prefixes(self, guild: discord.Guild) -> List[str]:
        """Get custom  prefixes for one guild.

        Parameters
        ----------
        guild:discord.Guild
            The required guild prefixes.

        Returns
        -------
        List[str]
            List of all prefixes.
        """
        core = self.__getitem__("core")
        prefixes = core.get("guild", {}).get(guild.id, {}).get("prefixes", [])

        return prefixes

    def get_blacklist(self, key: str) -> List[Union[str, int]]:
        """Return list off all blacklisted values

        Parameters
        ----------
        key:str
            Which type of blacklist to choice (guilds ? channels ?,...).

        Returns
        -------
        List[Union[str, int]]
            List containing blacklisted values.
        """
        core = self.__getitem__("core")
        blacklist = core.get("blacklist", {}).get(key, [])

        return blacklist

    def _dump(self):
        with self._settings_file.open("w") as f:
            json.dump(self._datas, f, indent=4)

    async def update(self, cog_name: str, item: str, value: Any) -> dict:
        """Update values in config file.

        Parameters
        ----------
        cog_name:str
            Name of cog who's corresponding to the config file.
        item:str
            Key to update.
        value:Any
            New values to apply.

        Returns
        -------
        dict:
            Updated values.

        """
        datas = self.__getitem__(cog_name)
        path = data_path(self._cog_instance)

        datas[item] = value

        self._datas = datas

        if cog_name != "core":
            path = path / "cogs" / cog_name
        else:
            path /= "core"

        self._settings_file = path / "settings.json"

        async with self.lock:
            await self.loop.run_in_executor(None, self._dump)

        return datas
