import logging
from typing import Optional

import discord
from discord.ext import commands, menus

from tuxbot.cogs.Tags.functions.converters import TagConverter, NewTagConverter
from tuxbot.cogs.Tags.functions.exceptions import (
    UnknownTagException,
    ExistingTagException,
    TooLongTagException,
    ReservedTagException,
)
from tuxbot.cogs.Tags.functions.paginator import TagPages
from tuxbot.cogs.Tags.functions.utils import (
    get_tag,
    get_all_tags,
    search_tags,
    create_tag,
    edit_tag,
)
from tuxbot.core.bot import Tux

from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.functions.extra import (
    group_extra,
    ContextPlus,
)

log = logging.getLogger("tuxbot.cogs.Tags")
_ = Translator("Tags", __file__)


class Tags(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def cog_command_error(self, ctx: ContextPlus, error):
        if isinstance(
            error,
            (
                UnknownTagException,
                ExistingTagException,
                TooLongTagException,
                ReservedTagException,
            ),
        ):
            await ctx.send(_(str(error), ctx, self.bot.config))

    # =========================================================================
    # =========================================================================

    @group_extra(name="tag", invoke_without_command=True, deletable=False)
    @commands.guild_only()
    async def _tag(self, ctx: ContextPlus, *, name: TagConverter):
        tag_row = await get_tag(ctx.guild.id, str(name))

        await ctx.send(tag_row.content)

        tag_row.uses += 1  # type: ignore

        await tag_row.save()

    @_tag.command(name="delete")
    async def _tag_delete(self, ctx: ContextPlus, *, name: TagConverter):
        tag_row = await get_tag(ctx.guild.id, str(name))

        backdoor = (
            await ctx.bot.is_owner(ctx.author)
            or ctx.author.guild_permissions.manage_messages
        )

        if backdoor or ctx.author.id == tag_row.id:
            await tag_row.delete()
            return await ctx.send(
                _("Tag successfully deleted", ctx, self.bot.config)
            )

        await ctx.send(_("Your can't delete this tag", ctx, self.bot.config))

    @_tag.command(name="create", aliases=["add"])
    async def _tag_create(
        self, ctx, name: NewTagConverter, *, content: commands.clean_content
    ):
        await create_tag(ctx, str(name), str(content))

        await ctx.send(_("Tag successfully created", ctx, self.bot.config))

    @_tag.command(name="edit")
    async def _tag_edit(
        self, ctx, name: TagConverter, *, content: commands.clean_content
    ):
        tag_row = await get_tag(ctx.guild.id, str(name))

        backdoor = (
            await ctx.bot.is_owner(ctx.author)
            or ctx.author.guild_permissions.manage_messages
        )

        if backdoor or ctx.author.id == tag_row.id:
            await edit_tag(ctx, str(name), str(content))
            return await ctx.send(
                _("Tag successfully edited", ctx, self.bot.config)
            )

        await ctx.send(_("Your can't edit this tag", ctx, self.bot.config))

    @_tag.command(name="info", aliases=["owner"])
    async def _tag_info(self, ctx: ContextPlus, *, name: TagConverter):
        tag_row = await get_tag(ctx.guild.id, str(name))

        e = discord.Embed(color=discord.Colour.blue())

        owner_id = tag_row.author_id
        e.title = tag_row.name
        e.timestamp = tag_row.created_at

        user = self.bot.get_user(owner_id) or (
            await self.bot.fetch_user(owner_id)
        )

        e.set_author(name=str(user), icon_url=user.avatar.url)

        e.add_field(
            name=_("Owner", ctx, self.bot.config), value=f"<@{owner_id}>"
        )
        e.add_field(name=_("Uses", ctx, self.bot.config), value=tag_row.uses)

        await ctx.send(embed=e)

    @_tag.command(name="search", aliases=["find"])
    async def _tag_search(
        self, ctx: ContextPlus, *, name: commands.clean_content
    ):
        q = str(name)

        if len(q) < 3:
            return await ctx.send(
                _(
                    "The search must be at least 3 characters",
                    ctx,
                    self.bot.config,
                )
            )

        tags = await search_tags(ctx.guild.id, q)

        if tags:
            try:
                p = TagPages(entries=tags)
                await p.start(ctx)
            except menus.MenuError as e:
                await ctx.send(e)
        else:
            await ctx.send(_("No tags found", ctx, self.bot.config))

    @_tag.command(name="list")
    async def _tag_list(
        self, ctx: ContextPlus, author: Optional[discord.Member]
    ):
        author = author or ctx.author

        tags = await get_all_tags(ctx.guild.id, author)

        if tags:
            try:
                p = TagPages(entries=tags)
                p.embed.set_author(
                    name=str(author), icon_url=author.avatar.url
                )
                await p.start(ctx)
            except menus.MenuError as e:
                await ctx.send(e)
        else:
            await ctx.send(
                _("No tags found for {}", ctx, self.bot.config).format(author)
            )

    @_tag.command(name="all")
    async def _tag_all(self, ctx: ContextPlus):
        tags = await get_all_tags(ctx.guild.id)

        if tags:
            try:
                p = TagPages(entries=tags)
                await p.start(ctx)
            except menus.MenuError as e:
                await ctx.send(e)
        else:
            await ctx.send(
                _("No tags found for {}", ctx, self.bot.config).format(
                    ctx.guild.name
                )
            )

    @_tag.command(name="claim")
    async def _tag_claim(self, ctx: ContextPlus, *, name: TagConverter):
        tag_row = await get_tag(ctx.guild.id, str(name))

        if await ctx.guild.fetch_member(tag_row.author_id) is not None:
            return await ctx.send(
                _("Tag owner is on this server.", ctx, self.bot.config)
            )

        tag_row.author_id = ctx.author.id

        await tag_row.save()

        await ctx.send(
            _("This tag is now owned by you.", ctx, self.bot.config)
        )
