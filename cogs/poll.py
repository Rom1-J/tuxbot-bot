from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts


class Poll(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    """---------------------------------------------------------------------"""

    @commands.group(name='sondage', aliases=['poll'])
    async def _poll(self, ctx):
        """
        todo: refer to readme.md
        """


def setup(bot: TuxBot):
    bot.add_cog(Poll(bot))
