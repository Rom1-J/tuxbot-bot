from typing import List

import discord

from tuxbot.core.bot import Tux


def get_prefixes(tux: Tux, guild: discord.Guild) -> List[str]:
    """Get custom  prefixes for one guild.
    Parameters
    ----------
    tux:Tux
        The bot instance.

    guild:discord.Guild
        The required guild prefixes.
    Returns
    -------
    List[str]
        List of all prefixes.
    """
    return tux.config.Servers.all[guild.id].prefixes or []
