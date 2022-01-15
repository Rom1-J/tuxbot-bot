"""
Discord status colors
"""
from enum import Enum

import discord


class Colors(Enum):
    """Enum of all different discord status colors"""
    ONLINE = discord.Color(0x3BA55D)
    IDLE = discord.Color(0xFAA81A)
    DND = discord.Color(0xED4245)
    STREAMING = discord.Color(0x593696)
    EMBED_BORDER = discord.Color(0x2F3136)
