from typing import Optional, List

import discord

from tuxbot.cogs.Tags.models import Tag
from tuxbot.core.utils.functions.extra import ContextPlus


async def get_tag(guild_id: int, name: str) -> Tag:
    return await Tag.get(server_id=guild_id, name=name)


async def get_all_tags(
    guild_id: int, author: Optional[discord.Member] = None
) -> List[Tag]:
    if author is not None:
        return (
            await Tag.filter(server_id=guild_id, author_id=author.id)
            .all()
            .order_by("-uses")
        )

    return await Tag.filter(server_id=guild_id).all().order_by("-uses")


async def search_tags(guild_id: int, q: str) -> List[Tag]:
    return (
        await Tag.filter(server_id=guild_id, name__icontains=q)
        .all()
        .order_by("-uses")
    )


async def create_tag(ctx: ContextPlus, name: str, content: str):
    tag_row = await Tag()

    tag_row.server_id = ctx.guild.id
    tag_row.author_id = ctx.author.id

    tag_row.name = name  # type: ignore
    tag_row.content = content  # type: ignore

    await tag_row.save()


async def edit_tag(ctx: ContextPlus, name: str, content: str):
    tag_row = await get_tag(ctx.guild.id, name)

    tag_row.content = content  # type: ignore

    await tag_row.save()
