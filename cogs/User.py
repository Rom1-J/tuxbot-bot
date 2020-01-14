import logging

from discord.ext import commands

from bot import TuxBot
from utils import AliasesModel
from utils import Texts
from utils import groupExtra

log = logging.getLogger(__name__)


class User(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot
        self.icon = ":bust_in_silhouette:"
        self.big_icon = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/233/bust-in-silhouette_1f464.png"

    ###########################################################################

    @groupExtra(name='alias', aliases=['aliases'], category='alias')
    async def _alias(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help('alias')

    @_alias.command(name='add', aliases=['set', 'new'])
    async def _alias_add(self, ctx: commands.Context, *, user_alias: str):
        is_global = False
        if '--global' in user_alias:
            is_global = True
            user_alias.replace('--global', '')

        user_alias = user_alias.split(' -> ')
        if len(user_alias) != 2:
            return await ctx.send_help('alias')

        command = user_alias[1]
        user_alias = user_alias[0]

        if self.bot.get_command(command) is None:
            return await ctx.send(Texts('user').get('Command not found'))

        alias = AliasesModel(
            user_id=ctx.author.id,
            alias=user_alias,
            command=command,
            guild="global" if is_global else str(ctx.guild.id)
        )

        self.bot.database.session.add(alias)
        self.bot.database.session.commit()

    @_alias.command(name='remove', aliases=['drop', 'del', 'delete'])
    async def _alias_remove(self, ctx: commands.Context, prefix: str):
        ...

    @_alias.command(name='list', aliases=['show', 'all'])
    async def _alias_list(self, ctx: commands.Context):
        ...


def setup(bot: TuxBot):
    bot.add_cog(User(bot))
