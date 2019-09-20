import datetime
from typing import Union

import discord
import humanize
from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts


class Admin(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot
        self.db = bot.db

    async def cog_check(self, ctx: commands.Context) -> bool:
        permissions: discord.Permissions = ctx.channel.permissions_for(
            ctx.author)

        has_permission = permissions.administrator
        is_owner = await self.bot.is_owner(ctx.author)

        return has_permission or is_owner

    @staticmethod
    async def kick_ban_message(ctx: commands.Context,
                               **kwargs) -> discord.Embed:
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

    @commands.group(name='say', invoke_without_command=True)
    async def _say(self, ctx: commands.Context, *, content: str):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        await ctx.send(content)

    @_say.command(name='edit')
    async def _say_edit(self, ctx: commands.Context, message_id: int, *,
                        content: str):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        try:
            message: discord.Message = await ctx.channel.fetch_message(
                message_id)
            await message.edit(content=content)
        except (discord.errors.NotFound, discord.errors.Forbidden):
            await ctx.send(Texts('utils').get("Unable to find the message"),
                           delete_after=5)

    @_say.command(name='to')
    async def _say_to(self, ctx: commands.Context,
                      channel: Union[discord.TextChannel, discord.User], *,
                      content):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        await channel.send(content)

    """---------------------------------------------------------------------"""

    @commands.command(name='ban')
    async def _ban(self, ctx: commands.Context, user: discord.User, *,
                   reason=""):
        try:
            member: discord.Member = await ctx.guild.fetch_member(user.id)

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
                await ctx.send(Texts('admin').get("Unable to ban this user"),
                               delete_after=5)
        except discord.errors.NotFound:
            await ctx.send(Texts('utils').get("Unable to find the user..."),
                           delete_after=5)

    """---------------------------------------------------------------------"""

    @commands.command(name='kick')
    async def _kick(self, ctx: commands.Context, user: discord.User, *,
                    reason=""):
        try:
            member: discord.Member = await ctx.guild.fetch_member(user.id)

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
                await ctx.send(Texts('admin').get("Unable to kick this user"),
                               delete_after=5)
        except discord.errors.NotFound:
            await ctx.send(Texts('utils').get("Unable to find the user..."),
                           delete_after=5)

    """---------------------------------------------------------------------"""

    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context, count: int):
        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=count)
        except discord.errors.Forbidden:
            pass

    """---------------------------------------------------------------------"""

    @commands.group(name='react')
    async def _react(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return

    @_react.command(name='add')
    async def _react_add(self, ctx: commands.Context, message_id: int, *,
                         emojis: str):
        emojis: list = emojis.split(' ')

        try:
            message: discord.Message = await ctx.channel.fetch_message(
                message_id)

            for emoji in emojis:
                await message.add_reaction(emoji)
        except discord.errors.NotFound:
            await ctx.send(Texts('utils').get("Unable to find the message"),
                           delete_after=5)

    @_react.command(name='clear')
    async def _react_remove(self, ctx: commands.Context, message_id: int):
        try:
            message: discord.Message = await ctx.channel.fetch_message(
                message_id)
            await message.clear_reactions()
        except discord.errors.NotFound:
            await ctx.send(Texts('utils').get("Unable to find the message"),
                           delete_after=5)

    """---------------------------------------------------------------------"""

    @commands.group(name='delete', invoke_without_command=True)
    async def _delete(self, ctx: commands.Context, message_id: int):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        try:
            message: discord.Message = await ctx.channel.fetch_message(
                message_id)
            await message.delete()
        except (discord.errors.NotFound, discord.errors.Forbidden):
            await ctx.send(Texts('utils').get("Unable to find the message"),
                           delete_after=5)

    @_delete.command(name='from', aliases=['to', 'in'])
    async def _delete_from(self, ctx: commands.Context,
                           channel: discord.TextChannel, message_id: int):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        try:
            message: discord.Message = await channel.fetch_message(
                message_id)
            await message.delete()
        except (discord.errors.NotFound, discord.errors.Forbidden):
            await ctx.send(Texts('utils').get("Unable to find the message"),
                           delete_after=5)

    """---------------------------------------------------------------------"""

    @commands.group(name='warn', aliases=['warns'])
    async def _warn(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            query = """
            SELECT user_id, reason, created_at FROM warns 
            WHERE created_at >= $1 AND server_id = $2
            ORDER BY created_at 
            DESC LIMIT 10
            """
            week_ago = datetime.datetime.now() - datetime.timedelta(weeks=6)

            async with self.bot.db.acquire() as con:
                await ctx.trigger_typing()
                warns = await con.fetch(query, week_ago, ctx.guild.id)
                warns_list = ''

                for warn in warns:
                    user_id = warn.get('user_id')
                    user = await self.bot.fetch_user(user_id)
                    reason = warn.get('reason')
                    ago = humanize.naturaldelta(
                        datetime.datetime.now() - warn.get('created_at')
                    )

                    warns_list += f"**{user}**: `{reason}` *({ago} ago)*\n"

                e = discord.Embed(
                    title=f"{len(warns)} {Texts('admin').get('last warns')}: ",
                    description=warns_list
                )

                await ctx.send(embed=e)

    @_warn.command(name='add', aliases=['new'])
    async def _warn_new(self, ctx: commands.Context, member: discord.Member,
                        *, reason):
        """
        todo: push in database
        if warn > 2 for member:
            todo: ask for confirmation to kick or ban
        """


def setup(bot: TuxBot):
    bot.add_cog(Admin(bot))
