import datetime

import discord
from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts


class Admin(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        permissions = ctx.channel.permissions_for(ctx.author)

        has_permission = permissions.administrator
        is_owner = await self.bot.is_owner(ctx.author)

        return has_permission or is_owner

    @staticmethod
    async def kick_ban_message(ctx: commands.Context, **kwargs) -> discord.Embed:
        member: discord.Member = kwargs.get('member')
        reason = kwargs.get(
            'reason',
            Texts('admin').get("Please enter a reason")
        )

        if kwargs.get('type') == 'ban':
            title = '**Ban** ' + str(len(await ctx.guild.bans()))
            color = discord.Color.dark_red()
        else:
            title = '**Kick**'
            color = discord.Color.red()
        e = discord.Embed(
            title=title,
            description=reason,
            timestamp=datetime.datetime.utcnow(),
            color=color
        )
        e.set_author(
            name=f'{member.name}#{member.discriminator} ({member.id})',
            icon_url=member.avatar_url_as(format='jpg')
        )
        e.set_footer(
            text=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url_as(format='png')
        )

        return e

    """---------------------------------------------------------------------"""

    @commands.command(name='say')
    async def _say(self, ctx: commands.Context, *, to_say: str):
        try:
            await ctx.message.delete()
            await ctx.send(to_say)
        except discord.errors.Forbidden:
            await ctx.send(to_say)

    """---------------------------------------------------------------------"""

    @commands.command(name="ban")
    async def _ban(self, ctx: commands.Context, user: discord.User, *,
                   reason=""):
        member: discord.Member = await ctx.guild.fetch_member(user.id)

        if member:
            try:
                await member.ban(reason=reason)
                e: discord.Embed = await self.kick_ban_message(
                    ctx,
                    member=member,
                    type='ban',
                    reason=reason
                )

                await ctx.send(embed=e)
            except discord.Forbidden:
                await ctx.send(Texts('admin').get("Unable to ban this user"))
        else:
            await ctx.send(Texts('admin').get("Unable to find the user..."))

    """---------------------------------------------------------------------"""

    @commands.command(name="kick")
    async def _kick(self, ctx: commands.Context, user: discord.User, *,
                    reason=""):
        member: discord.Member = await ctx.guild.fetch_member(user.id)

        if member:
            try:
                await member.kick(reason=reason)
                e: discord.Embed = await self.kick_ban_message(
                    ctx,
                    member=member,
                    type='kick',
                    reason=reason
                )

                await ctx.send(embed=e)
            except discord.Forbidden:
                await ctx.send(Texts('admin').get("Unable to ban this user"))
        else:
            await ctx.send(Texts('admin').get("Unable to find the user..."))

    """---------------------------------------------------------------------"""


def setup(bot: TuxBot):
    bot.add_cog(Admin(bot))
