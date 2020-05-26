import logging

from discord.ext import commands

from app import TuxBot
from utils.functions.extra import ContextPlus, command_extra

log = logging.getLogger(__name__)


class Useless(commands.Cog, name="Useless"):
    def __init__(self, bot):
        self.bot = bot

    @command_extra(name="space")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _space(self, ctx: ContextPlus):
        await ctx.send("""
        > ˚　　　　　　　　　　　　　　*　　　　　　   　　　　　　　　　　　　　　　.　　　　　　　　　　　　　　. 　　 　　　　　　　 ✦ 　　　　　　　　　　 　 ‍ ‍ ‍ ‍ 　　　　 　　　　　　　　　　　　,　　   　
        > 
        > .　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　　　　　　　　　　　.
        > 
        > 　　　　　　,　　　　　　　.　　　　　　    　　　　 　　　　　　　　　　　　　　　　　　 :sunny: 　　　　　　　　　　　　　　　　　　    　      　　　　　        　　　　　　　　　　　　　. 　　　　　　　　　　.　　　　　　　　　　　　　. 　　　　　　　　　　　　　　　　       　   　　　　 　　　　　　　　　　　　　　　　       　   　　　　　　　　　　　　　　　　       　    ✦ 　   　　　,　　　　　　　　　　　    :rocket: 　　　　 　　,　　　 ‍ ‍ ‍ ‍ 　 　　　　　　　　　　　　.　　　　　 　　 　　　.　　　　　　　　　　　　　 　           　　　　　　　　　　　　　　　　　　　˚　　　 　   　　　　,　　　　　　　　　　　       　    　　　　　　　　　　　　　　　　.　　　  　　    　　　　　 　　　　　.　　　　　　　　　　　　　.　　　　　　　　　　　　　　　* 　　   　　　　　 ✦ 　　　　　　　         　        　　　　 　　 　　　　　　　 　　　　　.　　　　　　　　　　　　　　　　　　.　　　　　    　　. 　 　　　　　.　　　　    :new_moon:  　　　　　   　　　　　.　　　　　　　　　　　.　　　　　　　　　　   　
        > 
        > 　˚　　　　　　　　　　　　　　　　　　　　　ﾟ　　　　　.　　　　　　　　　　　　　　　. 　　 　 :earth_americas: ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ,　 　　　　　　　　　　　　　　* .　　　　　 　　　　　　　　　　　　　　.　　　　　　　　　　 ✦ 　　　　   　 　　　˚　　　　　　　　　　　　　　　　　　　　   　　　　　　　　　　　　　　　.　　　　　　　　　　　　　　. .　　　　　　　　　　 ✦ 　　　　   　 　　　˚　　　　　　　　　　　　　　　　　　　　   　　　　　　　　　　　　　　　.　　　　　　　　　　　　　　. 　　 　　　　　　　 ✦ 　　　　　　　　　　 　 ‍ ‍ ‍ ‍ 　　　　 　　　　　　　　　　　　,　　   　
        > 
        > .　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　　　　　　　　　　　.
        """)


def setup(bot: TuxBot):
    cog = Useless(bot)
    bot.add_cog(cog)
