"""Simple paginator from embeds"""
import typing

import discord
from discord.ext import commands, menus

from tuxbot.abc.TuxbotABC import TuxbotABC

from .Pages import Pages


class SimplePages(Pages):
    """Simple paginator from embeds"""

    class SimplePageSource(menus.ListPageSource):
        """Source form SimplePages"""

        # pylint: disable=arguments-renamed
        async def format_page(
            self, menu: Pages, entries: typing.Any
        ) -> discord.Embed:
            """Format page before rendering"""

            pages = []

            for index, entry in enumerate(
                entries, start=menu.current_page * self.per_page
            ):
                pages.append(f"{index + 1}. {entry}")

            maximum = self.get_max_pages()  # type: ignore

            if maximum > 1:
                footer = (
                    f"Page {menu.current_page + 1}/{maximum} "
                    f"({len(self.entries)} entries)"
                )
                menu.embed.set_footer(text=footer)  # type: ignore

            menu.embed.description = "\n".join(pages)  # type: ignore
            return menu.embed  # type: ignore

    def __init__(
        self,
        entries: typing.Any,
        *,
        ctx: commands.Context[TuxbotABC] | discord.Interaction,
        per_page: int = 12,
    ):
        super().__init__(
            self.SimplePageSource(entries, per_page=per_page),  # type: ignore
            ctx=ctx,
        )
        self.embed = discord.Embed(colour=discord.Colour.blurple())
