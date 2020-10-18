from typing import List

import discord

from tuxbot.core.config import search_for


def get_prefixes(tux, guild: discord.Guild) -> List[str]:
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
    return search_for(tux.config.Servers, guild.id, "prefixes", [])
