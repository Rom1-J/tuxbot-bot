import json
import logging

__all__ = ["Config"]

from typing import List, Dict, Union

import discord

from tuxbot.core.data_manager import data_path

log = logging.getLogger("tuxbot.config")


class Config:
    def __init__(
            self,
            cog_instance: str = None
    ):
        self._cog_instance = cog_instance

    def __getitem__(self, item) -> Dict:
        path = data_path(self._cog_instance)

        if item != 'core':
            path = path / 'cogs' / item
        else:
            path /= 'core'

        settings_file = path / 'settings.json'

        if not settings_file.exists():
            raise FileNotFoundError(f"Unable to find settings file "
                                    f"'{settings_file}'")
        else:
            with settings_file.open('r') as f:
                return json.load(f)

    def __call__(self, item):
        return self.__getitem__(item)

    def owners_id(self) -> List[int]:
        return self.__getitem__('core').get('owners_id')

    def token(self) -> str:
        return self.__getitem__('core').get('token')

    def get_prefixes(self, guild: discord.Guild) -> List[str]:
        core = self.__getitem__('core')
        prefixes = core\
            .get('guild', {}) \
            .get(guild.id, {}) \
            .get('prefixes', [])

        return prefixes

    def get_blacklist(self, key: str) -> List[Union[str, int]]:
        core = self.__getitem__('core')
        blacklist = core \
            .get('blacklist', {}) \
            .get(key, [])

        return blacklist

    def update(self, cog_name, item, value) -> dict:
        datas = self.__getitem__(cog_name)
        path = data_path(self._cog_instance)

        datas[item] = value

        if cog_name != 'core':
            path = path / 'cogs' / cog_name
        else:
            path /= 'core'

        settings_file = path / 'settings.json'

        with settings_file.open('w') as f:
            json.dump(datas, f, indent=4)

        return datas
