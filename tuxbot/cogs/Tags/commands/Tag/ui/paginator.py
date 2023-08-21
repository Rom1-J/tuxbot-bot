import typing

import discord

from tuxbot.cogs.Tags.commands.Tag.models.tags import TagsModel
from tuxbot.core.utils.Paginator.simple_pages import SimplePages


class TagPage:
    """One page of tags."""

    def __init__(self: typing.Self, i: int, entry: TagsModel) -> None:
        self.id: int = i
        self.name: str = entry.name
        self.uses: int = entry.uses

    def __str__(self: typing.Self) -> str:
        return f"{self.name} ({self.uses})"


class TagPages(SimplePages):
    """All tags pages."""

    def __init__(
        self: typing.Self,
        entries: list[TagsModel],
        ctx: discord.Interaction,
        per_page: int = 15,
    ) -> None:
        super().__init__(
            [TagPage(i, entry) for i, entry in enumerate(entries)],
            ctx=ctx,
            per_page=per_page,
        )
