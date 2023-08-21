"""Simple paginator from embeds."""
import typing

import discord
from discord.ext import commands, menus

from tuxbot.abc.tuxbot_abc import TuxbotABC

from .pages import Pages


class SimplePages(Pages):
    """Simple paginator from embeds."""

    class SimplePageSource(menus.ListPageSource):
        """Source form SimplePages."""

        # pylint: disable=arguments-renamed
        async def format_page(
            self: typing.Self, menu: Pages, entries: typing.Iterable[object]
        ) -> discord.Embed:
            """Format page before rendering."""
            pages = []

            for index, entry in enumerate(
                entries, start=menu.current_page * self.per_page
            ):
                pages.append(f"{index + 1}. {entry}")

            maximum = self.get_max_pages()

            if maximum > 1:
                footer = (
                    f"Page {menu.current_page + 1}/{maximum} "
                    f"({len(self.entries)} entries)"
                )
                menu.embed.set_footer(text=footer)

            menu.embed.description = "\n".join(pages)
            return menu.embed

    def __init__(
        self: typing.Self,
        entries: typing.Iterable[object],
        *,
        ctx: commands.Context[TuxbotABC] | discord.Interaction,
        per_page: int = 12,
    ) -> None:
        super().__init__(
            self.SimplePageSource(entries, per_page=per_page),
            ctx=ctx,
        )
        self.embed = discord.Embed(colour=discord.Colour.blurple())
