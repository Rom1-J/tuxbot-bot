from discord.ext import commands
from bot import TuxBot


class Admin(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        permissions = ctx.channel.permissions_for(ctx.author)
        return permissions.administrator

    """---------------------------------------------------------------------"""

    @commands.command(name='say', pass_context=True)
    async def _say(self, ctx: commands.Context, *, to_say: str):
        # try:
        await ctx.message.delete()
        await ctx.send(to_say)
        # except:
        #     await ctx.send(to_say)


def setup(bot: TuxBot):
    bot.add_cog(Admin(bot))
