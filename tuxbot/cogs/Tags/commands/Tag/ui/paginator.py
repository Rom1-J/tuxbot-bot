import discord

from tuxbot.core.utils.Paginator.SimplePages import SimplePages

from ..models.Tags import TagsModel


class TagPage:
    """One page of tags"""

    def __init__(self, i: int, entry: TagsModel) -> None:
        self.id: int = i
        self.name: str = entry.name
        self.uses: int = entry.uses

    def __str__(self) -> str:
        return f"{self.name} ({self.uses})"


class TagPages(SimplePages):
    """All tags pages"""

    def __init__(
        self,
        entries: list[TagsModel],
        ctx: discord.Interaction,
        per_page: int = 15,
    ) -> None:
        super().__init__(
            [TagPage(i, entry) for i, entry in enumerate(entries)],
            ctx=ctx,
            per_page=per_page,
        )
