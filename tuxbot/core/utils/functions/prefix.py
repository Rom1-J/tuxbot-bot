from typing import List, Optional

import discord

from tuxbot.core.config import search_for


def get_prefixes(tux, guild: Optional[discord.Guild]) -> List[str]:
    """Get custom  prefixes for one guild.
    Parameters
    ----------
    tux:Tux
        The bot instance.

    guild:Optional[discord.Guild]
        The required guild prefixes.
    Returns
    -------
    List[str]
        List of all prefixes.
    """
    if not guild:
        return []
    return search_for(tux.config.Servers, guild.id, "prefixes", [])
