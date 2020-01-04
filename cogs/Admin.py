import asyncio
import datetime
import logging
from typing import Union

import discord
import humanize
from discord.ext import commands

from bot import TuxBot
from utils import Texts
from utils import WarnModel, LangModel
from utils import commandExtra, groupExtra

log = logging.getLogger(__name__)


class Admin(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot
        self.icon = ":shield:"
        self.big_icon = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/233/shield_1f6e1.png"

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
            Texts('admin', ctx).get("Please enter a reason")
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

    ###########################################################################

    @groupExtra(name='say', invoke_without_command=True, category='admin',
                description=Texts('admin_help').get('_say'))
    async def _say(self, ctx: commands.Context, *, content: str):
        if ctx.invoked_subcommand is None:
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                pass

            await ctx.send(content)

    @_say.command(name='edit',
                  description=Texts('admin_help').get('_say_edit'))
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
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the message"),
                delete_after=5)

    @_say.command(name='to',
                  description=Texts('admin_help').get('_say_to'))
    async def _say_to(self, ctx: commands.Context,
                      channel: Union[discord.TextChannel, discord.User], *,
                      content):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        await channel.send(content)

    ###########################################################################

    @commandExtra(name='ban', category='admin',
                  description=Texts('admin_help').get('_ban'))
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
                await ctx.send(
                    Texts('admin', ctx).get("Unable to ban this user"),
                    delete_after=5)
        except discord.errors.NotFound:
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the user..."),
                delete_after=5)

    ###########################################################################

    @commandExtra(name='kick', category='admin',
                  description=Texts('admin_help').get('_kick'))
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
                await ctx.send(
                    Texts('admin', ctx).get("Unable to kick this user"),
                    delete_after=5)
        except discord.errors.NotFound:
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the user..."),
                delete_after=5)

    ###########################################################################

    @commandExtra(name='clear', category='admin',
                  description=Texts('admin_help').get('_clear'))
    async def _clear(self, ctx: commands.Context, count: int):
        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=count)
        except discord.errors.Forbidden:
            pass

    ###########################################################################

    @groupExtra(name='react', category='admin',
                description=Texts('admin_help').get('_react'))
    async def _react(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help('react')

    @_react.command(name='add',
                    description=Texts('admin_help').get('admin._react_add'))
    async def _react_add(self, ctx: commands.Context, message_id: int, *,
                         emojis: str):
        emojis: list = emojis.split(' ')

        try:
            message: discord.Message = await ctx.channel.fetch_message(
                message_id)

            for emoji in emojis:
                await message.add_reaction(emoji)
        except discord.errors.NotFound:
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the message"),
                delete_after=5)

    @_react.command(name='clear',
                    description=Texts('admin_help').get('_react_remove'))
    async def _react_remove(self, ctx: commands.Context, message_id: int):
        try:
            message: discord.Message = await ctx.channel.fetch_message(
                message_id)
            await message.clear_reactions()
        except discord.errors.NotFound:
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the message"),
                delete_after=5)

    ###########################################################################

    @groupExtra(name='delete', invoke_without_command=True,
                category='admin',
                description=Texts('admin_help').get('_delete'))
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
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the message"),
                delete_after=5)

    @_delete.command(name='from', aliases=['to', 'in'],
                     description=Texts('admin_help').get('_delete_from'))
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
            await ctx.send(
                Texts('utils', ctx).get("Unable to find the message"),
                delete_after=5)

    ###########################################################################

    async def get_warn(self, ctx: commands.Context,
                       member: discord.Member = False):
        await ctx.trigger_typing()

        week_ago = datetime.datetime.now() - datetime.timedelta(weeks=6)

        if member:
            warns = self.bot.database.session \
                .query(WarnModel) \
                .filter(WarnModel.user_id == member.id, WarnModel.created_at > week_ago,
                        WarnModel.server_id == ctx.guild.id) \
                .order_by(WarnModel.created_at.desc())
        else:
            warns = self.bot.database.session \
                .query(WarnModel) \
                .filter(WarnModel.created_at > week_ago,
                        WarnModel.server_id == ctx.guild.id) \
                .order_by(WarnModel.created_at.desc())
        warns_list = ''

        for warn in warns:
            row_id = warn.id
            user_id = warn.user_id
            user = await self.bot.fetch_user(user_id)
            reason = warn.reason
            ago = humanize.naturaldelta(
                datetime.datetime.now() - warn.created_at
            )

            warns_list += f"[{row_id}] **{user}**: `{reason}` *({ago} ago)*\n"

        return warns_list, warns

    async def add_warn(self, ctx: commands.Context, member: discord.Member,
                       reason):

        now = datetime.datetime.now()
        warn = WarnModel(server_id=ctx.guild.id, user_id=member.id, reason=reason,
                         created_at=now)

        self.bot.database.session.add(warn)
        self.bot.database.session.commit()

    @groupExtra(name='warn', aliases=['warns'], category='admin',
                description=Texts('admin_help').get('_warn'))
    async def _warn(self, ctx: commands.Context):
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            warns_list, warns = await self.get_warn(ctx)
            e = discord.Embed(
                title=f"{warns.count()} {Texts('admin', ctx).get('last warns')}: ",
                description=warns_list
            )

            await ctx.send(embed=e)

    @_warn.command(name='add', aliases=['new'],
                   description=Texts('admin_help').get('_warn_new'))
    async def _warn_new(self, ctx: commands.Context, member: discord.Member,
                        *, reason="N/A"):
        member = await ctx.guild.fetch_member(member.id)
        if not member:
            return await ctx.send(
                Texts('utils', ctx).get("Unable to find the user...")
            )

        def check(pld: discord.RawReactionActionEvent):
            if pld.message_id != choice.id \
                    or pld.user_id != ctx.author.id:
                return False
            return pld.emoji.name in ('1⃣', '2⃣', '3⃣')

        warns_list, warns = await self.get_warn(ctx)

        if warns.count() >= 3:
            e = discord.Embed(
                title=Texts('admin', ctx).get('More than 2 warns'),
                description=f"{member.mention} "
                            + Texts('admin', ctx).get('has more than 2 warns')
            )
            e.add_field(
                name='__Actions__',
                value=':one: kick\n'
                      ':two: ban\n'
                      ':three: ' + Texts('admin', ctx).get('ignore')
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
                    Texts('admin', ctx).get('Took too long. Aborting.')
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
                            f"{Texts('admin', ctx).get('More than 2 warns')}"
                )
                return await alt_ctx.command.invoke(alt_ctx)

            elif payload.emoji.name == '2⃣':
                from jishaku.models import copy_context_with

                alt_ctx = await copy_context_with(
                    ctx,
                    content=f"{ctx.prefix}"
                            f"ban "
                            f"{member} "
                            f"{Texts('admin', ctx).get('More than 2 warns')}"
                )
                return await alt_ctx.command.invoke(alt_ctx)

        await self.add_warn(ctx, member, reason)
        await ctx.send(
            content=f"{member.mention} "
                    f"**{Texts('admin', ctx).get('got a warn')}**"
                    f"\n**{Texts('admin', ctx).get('Reason')}:** `{reason}`"
        )

    @_warn.command(name='remove', aliases=['revoke', 'del', 'delete'],
                   description=Texts('admin_help').get('_warn_remove'))
    async def _warn_remove(self, ctx: commands.Context, warn_id: int):
        warn = self.bot.database.session \
            .query(WarnModel) \
            .filter(WarnModel.id == warn_id) \
            .one()

        self.bot.database.session.delete(warn)

        await ctx.send(f"{Texts('admin', ctx).get('Warn with id')} `{warn_id}`"
                       f" {Texts('admin', ctx).get('successfully removed')}")

    @_warn.command(name='show', aliases=['list', 'all'],
                   description=Texts('admin_help').get('_warn_show'))
    async def _warn_show(self, ctx: commands.Context, member: discord.Member):
        warns_list, warns = await self.get_warn(ctx, member)

        e = discord.Embed(
            title=f"{warns.count()} {Texts('admin', ctx).get('last warns')}: ",
            description=warns_list
        )

        await ctx.send(embed=e)

    @_warn.command(name='edit', aliases=['change', 'modify'],
                   description=Texts('admin_help').get('_warn_edit'))
    async def _warn_edit(self, ctx: commands.Context, warn_id: int, *, reason):
        warn = self.bot.database.session \
            .query(WarnModel) \
            .filter(WarnModel.id == warn_id) \
            .one()
        warn.reason = reason

        self.bot.database.session.commit()

        await ctx.send(f"{Texts('admin', ctx).get('Warn with id')} `{warn_id}`"
                       f" {Texts('admin', ctx).get('successfully edited')}")

    ###########################################################################

    @commandExtra(name='language', aliases=['lang', 'langue', 'langage'],
                  category='admin',
                  description=Texts('admin_help').get('_language'))
    async def _language(self, ctx: commands.Context, locale: str):
        available = self.bot.database.session \
            .query(LangModel.value) \
            .filter(LangModel.key == 'available') \
            .first()[0] \
            .split(',')

        if locale.lower() not in available:
            await ctx.send(
                Texts('admin', ctx).get('Unable to find this language'))
        else:
            current = self.bot.database.session \
                .query(LangModel) \
                .filter(LangModel.key == str(ctx.guild.id))

            if current.count() > 0:
                current = current.one()
                current.value = locale.lower()
                self.bot.database.session.commit()
            else:
                new_row = LangModel(key=str(ctx.guild.id), value=locale.lower())
                self.bot.database.session.add(new_row)
                self.bot.database.session.commit()

            await ctx.send(
                Texts('admin', ctx).get('Language changed successfully'))

    ###########################################################################

    @groupExtra(name='prefix', aliases=['prefixes'], category='admin',
                description=Texts('admin_help').get('_prefix'))
    async def _prefix(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help('prefix')

    @_prefix.command(name='add', aliases=['set', 'new'],
                     description=Texts('admin_help').get('_prefix_add'))
    async def _prefix_add(self, ctx: commands.Context, prefix: str):
        if str(ctx.guild.id) in self.bot.prefixes:
            prefixes = self.bot.prefixes.get(
                str(ctx.guild.id), "prefixes"
            ).split(
                self.bot.config.get("misc", "separator")
            )

            if prefix in prefixes:
                return await ctx.send(
                    Texts('admin', ctx).get('This prefix already exists')
                )
            else:
                prefixes.append(prefix)
                self.bot.prefixes.set(
                    str(ctx.guild.id),
                    "prefixes",
                    self.bot.config.get("misc", "separator")
                        .join(prefixes)
                )
                with open('./configs/prefixes.cfg', 'w') as configfile:
                    self.bot.prefixes.write(configfile)
        else:
            self.bot.prefixes.add_section(str(ctx.guild.id))
            self.bot.prefixes.set(str(ctx.guild.id), "prefixes", prefix)
            with open('./configs/prefixes.cfg', 'w') as configfile:
                self.bot.prefixes.write(configfile)

        await ctx.send(
            Texts('admin', ctx).get('Prefix added successfully')
        )

    @_prefix.command(name='remove', aliases=['drop', 'del', 'delete'],
                     description=Texts('admin_help').get('_prefix_remove'))
    async def _prefix_remove(self, ctx: commands.Context, prefix: str):
        if str(ctx.guild.id) in self.bot.prefixes:
            prefixes = self.bot.prefixes.get(
                str(ctx.guild.id), "prefixes"
            ).split(
                self.bot.config.get("misc", "separator")
            )

            if prefix in prefixes:
                prefixes.remove(prefix)
                self.bot.prefixes.set(
                    str(ctx.guild.id),
                    "prefixes",
                    self.bot.config.get("misc", "separator")
                        .join(prefixes)
                )
                with open('./configs/prefixes.cfg', 'w') as configfile:
                    self.bot.prefixes.write(configfile)

                return await ctx.send(
                    Texts('admin', ctx).get('Prefix removed successfully')
                )

        await ctx.send(
            Texts('admin', ctx).get('This prefix does not exist')
        )

    @_prefix.command(name='list', aliases=['show', 'all'],
                     description=Texts('admin_help').get('_prefix_list'))
    async def _prefix_list(self, ctx: commands.Context):
        extras = ['.']
        if ctx.message.guild is not None:
            extras = []
            if str(ctx.message.guild.id) in self.bot.prefixes:
                extras.extend(
                    self.bot.prefixes.get(str(ctx.message.guild.id),
                                          "prefixes").split(
                        self.bot.config.get("misc", "separator")
                    )
                )

        prefixes = [self.bot.user.mention]
        prefixes.extend(extras)

        if len(prefixes) <= 1:
            text = Texts('admin', ctx)\
                .get('The only prefix for this guild is :\n')
        else:
            text = Texts('admin', ctx)\
                .get('Available prefixes for this guild are :\n')

        await ctx.send(text + "\n • ".join(prefixes))


def setup(bot: TuxBot):
    bot.add_cog(Admin(bot))
