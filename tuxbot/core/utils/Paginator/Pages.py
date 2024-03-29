"""
Main paginator constructor
"""
import asyncio
import typing

import discord
from discord.ext import commands, menus

from tuxbot.abc.TuxbotABC import TuxbotABC


class Pages(discord.ui.View):
    """Main paginator constructor"""

    def __init__(
        self,
        source: menus.PageSource,
        *,
        ctx: commands.Context[TuxbotABC] | discord.Interaction,
    ):
        super().__init__()
        self.source: menus.PageSource = source
        self.ctx: commands.Context[TuxbotABC] | discord.Interaction = ctx

        self.message: discord.Message | None = None
        self.author: discord.Member | discord.User | None = None

        self.current_page: int = 0
        self.input_lock = asyncio.Lock()

        if isinstance(self.ctx, commands.Context):
            self.author = self.ctx.author
        elif isinstance(self.ctx, discord.Interaction):
            self.author = self.ctx.user

        self.clear_items()
        self.fill_items()

    def fill_items(self) -> None:
        """Generate items"""

        if self.source.is_paginating():  # type: ignore
            max_pages = self.source.get_max_pages()  # type: ignore
            use_last_and_first = max_pages is not None and max_pages >= 2

            if use_last_and_first:
                self.add_item(self.go_to_first_page)

            self.add_item(self.go_to_previous_page)
            self.add_item(self.go_to_current_page)
            self.add_item(self.go_to_next_page)

            if use_last_and_first:
                self.add_item(self.go_to_last_page)

            if isinstance(self.ctx, commands.Context):
                self.add_item(self.stop_pages)

    async def _get_kwargs_from_page(self, page: int) -> dict[str, typing.Any]:
        value: typing.Any = await discord.utils.maybe_coroutine(
            self.source.format_page, self, page  # type: ignore
        )

        if isinstance(value, dict):
            return value

        if isinstance(value, str):
            return {"content": value, "embed": None}

        if isinstance(value, discord.Embed):
            return {"embed": value, "content": None}

        return {}

    async def show_page(
        self, interaction: discord.Interaction, page_number: int
    ) -> None:
        """Send page"""

        page = await self.source.get_page(page_number)  # type: ignore
        self.current_page = page_number

        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(page_number)

        if kwargs:
            if interaction.response.is_done():
                if self.message:
                    await self.message.edit(**kwargs, view=self)
            else:
                await interaction.response.edit_message(**kwargs, view=self)

    def _update_labels(self, page_number: int) -> None:
        self.go_to_first_page.disabled = page_number == 0

        self.go_to_previous_page.disabled = False
        self.go_to_previous_page.label = str(page_number)

        self.go_to_current_page.label = str(page_number + 1)

        self.go_to_next_page.label = str(page_number + 2)
        self.go_to_next_page.disabled = False

        max_pages = self.source.get_max_pages()  # type: ignore

        if max_pages is not None:
            self.go_to_last_page.disabled = (page_number + 1) >= max_pages

            if (page_number + 1) >= max_pages:
                self.go_to_next_page.disabled = True
                self.go_to_next_page.label = "…"

            if page_number == 0:
                self.go_to_previous_page.disabled = True
                self.go_to_previous_page.label = "…"

    async def show_checked_page(
        self, interaction: discord.Interaction, page_number: int
    ) -> None:
        """Check before show page"""

        max_pages = self.source.get_max_pages()  # type: ignore

        try:
            if max_pages is None:
                await self.show_page(interaction, page_number)
                return

            if max_pages > page_number >= 0:
                await self.show_page(interaction, page_number)
                return
        except IndexError:
            pass

    async def interaction_check(
        self, interaction: discord.Interaction
    ) -> bool:
        """Ensure interaction is piloted by author"""
        if (
            interaction.user
            and self.author
            and interaction.user.id == self.author.id
        ):
            return True

        await interaction.response.send_message(
            "You aren't the author of this interaction.", ephemeral=True
        )
        return False

    async def on_timeout(self) -> None:
        """Clear message when timed out"""
        if self.message:
            await self.message.edit(view=None)

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item["Pages"],
    ) -> None:
        """Unknown error occurred"""

        if interaction.response.is_done():
            await interaction.followup.send(
                "Oops! Something went wrong.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Oops! Something went wrong.", ephemeral=True
            )

        if isinstance(self.ctx, commands.Context):
            self.ctx.bot.logger.error(error)

    async def start(self, *, content: str | None = None) -> None:
        """Start paginator"""

        # noinspection PyProtectedMember
        await self.source._prepare_once()  # type: ignore
        page = await self.source.get_page(0)  # type: ignore
        kwargs = await self._get_kwargs_from_page(page)

        if content:
            kwargs.setdefault("content", content)

        self._update_labels(0)

        if isinstance(self.ctx, commands.Context):
            self.message = await self.ctx.send(**kwargs, view=self)
            return

        if isinstance(self.ctx, discord.Interaction):
            await self.ctx.response.send_message(
                **kwargs, view=self, ephemeral=True
            )

    # =========================================================================

    # pylint: disable=unused-argument
    @discord.ui.button(label="≪", style=discord.ButtonStyle.grey)
    async def go_to_first_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["Pages"],
    ) -> None:
        """Go to the first page"""
        await self.show_page(interaction, 0)

    # =========================================================================

    # pylint: disable=unused-argument
    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple)
    async def go_to_previous_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["Pages"],
    ) -> None:
        """Go to the previous page"""
        await self.show_checked_page(interaction, self.current_page - 1)

    # =========================================================================

    # pylint: disable=unused-argument
    @discord.ui.button(
        label="Current", style=discord.ButtonStyle.grey, disabled=True
    )
    async def go_to_current_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["Pages"],
    ) -> None:
        """Go to the current page"""

    # =========================================================================

    # pylint: disable=unused-argument
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def go_to_next_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["Pages"],
    ) -> None:
        """Go to the next page"""
        await self.show_checked_page(interaction, self.current_page + 1)

    # =========================================================================

    # pylint: disable=unused-argument
    @discord.ui.button(label="≫", style=discord.ButtonStyle.grey)
    async def go_to_last_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["Pages"],
    ) -> None:
        """Go to the last page"""
        await self.show_page(
            interaction, self.source.get_max_pages() - 1  # type: ignore
        )

    # =========================================================================

    # pylint: disable=unused-argument
    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red, row=1)
    async def stop_pages(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["Pages"],
    ) -> None:
        """Stop the paginator"""
        await interaction.response.defer()
        await interaction.delete_original_response()

        self.stop()
