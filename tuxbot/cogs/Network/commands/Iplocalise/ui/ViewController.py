"""
Page view controller
"""
import asyncio
import json
import typing

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC

from ..providers.base import get_auxiliary_providers, get_base_providers
from .buttons import ButtonType
from .pages.GeoEmbed import GeoEmbed
from .pages.GlobalEmbed import GlobalEmbed
from .panels import ViewPanel


DATA_TYPE = typing.Union[str, int, float, dict, list]


class ViewController(discord.ui.View):
    """View controller"""

    __message: discord.Message | None = None
    __page: int = 0
    children: list[ButtonType]  # type: ignore

    def __init__(
        self,
        ctx: commands.Context[TuxbotABC],
        data: dict[str, typing.Any],
    ):
        super().__init__(timeout=60)

        self.ctx = ctx

        self.data = data
        self.embeds = [
            GlobalEmbed(self),
            GeoEmbed(self),
        ]

        self.__cache_key = self.ctx.bot.utils.gen_key(
            self.get_data("domain"), self.get_data("ip")
        )
        panel = ViewPanel.buttons

        for x, row in enumerate(panel):
            for button in row:
                self.add_item(button(row=x, controller=self))

    # =========================================================================
    # =========================================================================

    async def on_timeout(self) -> None:
        """Remove buttons after timeout"""

        self.clear_items()

        await self.edit()

    # =========================================================================

    async def interaction_check(
        self, interaction: discord.Interaction
    ) -> bool:
        """Ensure interaction is piloted by author"""

        if (
            interaction.user
            and self.ctx.author
            and interaction.user.id == self.ctx.author.id
        ):
            return True

        await interaction.response.send_message(
            "You aren't the author of this interaction.", ephemeral=True
        )
        return False

    # =========================================================================
    # =========================================================================

    async def __run_batch(self, batch: dict[str, DATA_TYPE]) -> None:
        tasks = []

        for name, provider in batch.items():
            if isinstance(provider, asyncio.Task):
                tasks.append(provider)
                continue

            self.data[name] = provider

        for task in asyncio.as_completed(tasks):
            await self.update(await task)

    # =========================================================================

    def get_data(self, provider: str, *args: typing.Any) -> DATA_TYPE:
        """Get data if available"""

        data: DATA_TYPE = self.data.get(provider, "Pending...")

        if data != "Pending...":
            for arg in args:
                if isinstance(data, (list, dict)) and arg in data:
                    data = data[arg]
                    continue

                data = "N/A"
                break

        return data

    # =========================================================================

    def get_button(self, name: str) -> ButtonType | None:
        """Get view button"""

        for button in self.children:
            if (button.label == name) or (
                button.emoji and button.emoji.name == name
            ):
                return button

        return None

    # =========================================================================

    async def change_page(
        self, new_page: int, interaction: discord.Interaction
    ) -> None:
        """Change current page"""
        self.__page = new_page

        await self.edit()
        await interaction.response.defer()

    # =========================================================================
    # =========================================================================

    async def update(self, result: tuple[str, dict[str, DATA_TYPE]]) -> None:
        """Update embed"""

        name, data = result

        self.data[name] = data
        for embed in self.embeds:
            embed.update(self)

        await self.edit()

    # =========================================================================

    async def send(self) -> None:
        """Send selected embed"""

        if data := await self.ctx.bot.redis.get(self.__cache_key):
            self.data = json.loads(data)
        else:
            await self.__run_batch(get_base_providers(self.data))
            await self.__run_batch(get_auxiliary_providers(self.data))
            await self.cache()

        if bgp_button := self.get_button("BGP toolkit"):
            bgp_button.disabled = False
            bgp_button.url = "https://bgp.he.net/AS" + str(  # type: ignore
                self.get_data("ipwhois", "asn")
            )

        if ipinfo_button := self.get_button("ipinfo.io"):
            ipinfo_button.disabled = False
            ipinfo_button.url = "https://ipinfo.io/" + str(  # type: ignore
                self.get_data("ip")
            )

        await self.edit()

    # =========================================================================

    async def edit(self) -> None:
        """Edit sent message"""
        embeds = [e.rebuild() for e in self.embeds]
        embed = embeds[self.__page]

        if self.__message:
            await self.__message.edit(embed=embed, view=self)
            return

        self.__message = await self.ctx.send(embed=embed, view=self)

    # =========================================================================

    async def cache(self) -> None:
        """Cache result"""
        await self.ctx.bot.redis.set(
            self.__cache_key, json.dumps(self.data), ex=3600 * 24
        )

    # =========================================================================

    async def delete(self) -> None:
        """Delete controller"""
        self.stop()

        if self.__message:
            await self.__message.delete()
