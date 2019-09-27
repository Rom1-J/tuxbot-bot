import datetime
import logging
from typing import Union

import asyncio
import discord
import humanize
from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts

log = logging.getLogger(__name__)


class Admin(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

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
    async def _ban(self, ctx: commands.Context, user: discord.Member, *,
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
    async def _kick(self, ctx: commands.Context, user: discord.Member, *,
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

    async def get_warn(self, ctx: commands.Context,
                       member: discord.Member = False):
        query = """
        SELECT * FROM warns 
        WHERE created_at >= $1 AND server_id = $2 
        """
        query += """AND user_id = $3""" if member else ""
        query += """ORDER BY created_at DESC"""
        week_ago = datetime.datetime.now() - datetime.timedelta(weeks=6)

        async with self.bot.db.acquire() as con:
            await ctx.trigger_typing()
            args = [week_ago, ctx.guild.id]
            if member:
                args.append(member.id)

            warns = await con.fetch(query, *args)
            warns_list = ''

            for warn in warns:
                row_id = warn.get('id')
                user_id = warn.get('user_id')
                user = await self.bot.fetch_user(user_id)
                reason = warn.get('reason')
                ago = humanize.naturaldelta(
                    datetime.datetime.now() - warn.get('created_at')
                )

                warns_list += f"[{row_id}] **{user}**: `{reason}` " \
                              f"*({ago} ago)*\n"

        return warns_list, warns

    @commands.group(name='warn', aliases=['warns'])
    async def _warn(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            warns_list, warns = await self.get_warn(ctx)
            e = discord.Embed(
                title=f"{len(warns)} {Texts('admin').get('last warns')}: ",
                description=warns_list
            )

            await ctx.send(embed=e)

    async def add_warn(self, ctx: commands.Context, member: discord.Member,
                       reason):

        query = """
        INSERT INTO warns (server_id, user_id, reason, created_at)
        VALUES ($1, $2, $3, $4)
        """

        now = datetime.datetime.now()
        await self.bot.db.execute(query, ctx.guild.id, member.id, reason, now)

    @_warn.command(name='add', aliases=['new'])
    async def _warn_new(self, ctx: commands.Context, member: discord.Member,
                        *, reason="N/A"):

        member = await ctx.guild.fetch_member(member.id)
        if not member:
            return await ctx.send(
                Texts('utils').get("Unable to find the user...")
            )

        query = """
        SELECT user_id, reason, created_at FROM warns 
        WHERE created_at >= $1 AND server_id = $2 and user_id = $3
        """
        week_ago = datetime.datetime.now() - datetime.timedelta(weeks=6)

        def check(payload: discord.RawReactionActionEvent):
            if payload.message_id != choice.id \
                    or payload.user_id != ctx.author.id:
                return False
            return payload.emoji.name in ('1⃣', '2⃣', '3⃣')

        async with self.bot.db.acquire() as con:
            await ctx.trigger_typing()
            warns = await con.fetch(query, week_ago, ctx.guild.id, member.id)

            if len(warns) >= 2:
                e = discord.Embed(
                    title=Texts('admin').get('More than 2 warns'),
                    description=f"{member.mention} "
                                + Texts('admin').get('has more than 2 warns')
                )
                e.add_field(
                    name='__Actions__',
                    value=':one: kick\n'
                          ':two: ban\n'
                          ':three: ' + Texts('admin').get('ignore')
                )

                choice = await ctx.send(embed=e)

                for reaction in ('1⃣', '2⃣', '3⃣'):
                    await choice.add_reaction(reaction)

                try:
                    payload = await self.bot.wait_for(
                        'raw_reaction_add',
                        check=check,
                        timeout=50.0
                    )
                except asyncio.TimeoutError:
                    return await ctx.send(
                        Texts('admin').get('Took too long. Aborting.')
                    )
                finally:
                    await choice.delete()

                if payload.emoji.name == '1⃣':
                    from jishaku.models import copy_context_with

                    alt_ctx = await copy_context_with(
                        ctx,
                        content=f"{ctx.prefix}"
                                f"kick "
                                f"{member} "
                                f"{Texts('admin').get('More than 2 warns')}"
                    )
                    return await alt_ctx.command.invoke(alt_ctx)

                elif payload.emoji.name == '2⃣':
                    from jishaku.models import copy_context_with

                    alt_ctx = await copy_context_with(
                        ctx,
                        content=f"{ctx.prefix}"
                                f"ban "
                                f"{member} "
                                f"{Texts('admin').get('More than 2 warns')}"
                    )
                    return await alt_ctx.command.invoke(alt_ctx)

            await self.add_warn(ctx, member, reason)
            await ctx.send(
                content=f"{member.mention} **{Texts('admin').get('got a warn')}**"
                f"\n**{Texts('admin').get('Reason')}:** `{reason}`"
                if reason != 'N/A' else ''
            )

    @_warn.command(name='remove', aliases=['revoke'])
    async def _warn_remove(self, ctx: commands.Context, warn_id: int):
        query = """
        DELETE FROM warns 
        WHERE id = $1
        """

        async with self.bot.db.acquire() as con:
            await ctx.trigger_typing()
            await con.fetch(query, warn_id)

        await ctx.send(f"{Texts('admin').get('Warn with id')} `{warn_id}`"
                       f" {Texts('admin').get('successfully removed')}")

    @_warn.command(name='show', aliases=['list'])
    async def _warn_show(self, ctx: commands.Context, member: discord.Member):
        warns_list, warns = await self.get_warn(ctx, member)
        e = discord.Embed(
            title=f"{len(warns)} {Texts('admin').get('last warns')}: ",
            description=warns_list
        )

        await ctx.send(embed=e)

    @_warn.command(name='edit', aliases=['change'])
    async def _warn_edit(self, ctx: commands.Context, warn_id: int, *,
                           reason):
        query = """
            UPDATE warns 
            SET reason = $2 
            WHERE id = $1
            """

        async with self.bot.db.acquire() as con:
            await ctx.trigger_typing()
            await con.fetch(query, warn_id, reason)

        await ctx.send(f"{Texts('admin').get('Warn with id')} `{warn_id}`"
                       f" {Texts('admin').get('successfully edited')}")

    """---------------------------------------------------------------------"""

    @commands.command(name='set-language', aliases=['set-lang'])
    async def _set_language(self, ctx: commands.Context, lang):
        """
        todo: set lang for guild
        """

def setup(bot: TuxBot):
    bot.add_cog(Admin(bot))
