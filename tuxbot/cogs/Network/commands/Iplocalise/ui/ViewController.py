"""
Page view controller
"""
import asyncio
import json
from typing import Optional, Tuple, Union

import discord
from discord.ext import commands

from ..providers.base import get_auxiliary_providers, get_base_providers
from .pages.GeoEmbed import GeoEmbed
from .pages.GlobalEmbed import GlobalEmbed
from .panels import ViewPanel


DATA_TYPE = Union[str, int, float, dict, list]


class ViewController(discord.ui.View):
    """View controller"""

    __message: discord.Message = None
    __page: int = 0

    def __init__(self, ctx: commands.Context, config: dict, data: dict):
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
        self.__config = config

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

        if interaction.user and self.ctx.author \
                and interaction.user.id == self.ctx.author.id:
            return True

        await interaction.response.send_message(
            "You aren't the author of this interaction.",
            ephemeral=True
        )
        return False

    # =========================================================================
    # =========================================================================

    async def __run_batch(self, batch):
        tasks = []

        for name, provider in batch.items():
            if isinstance(provider, asyncio.Task):
                tasks.append(provider)
                continue

            self.data[name] = provider

        for task in asyncio.as_completed(tasks):
            await self.update(await task)

    # =========================================================================

    def get_data(self, provider: str, *args) -> DATA_TYPE:
        """Get data if available"""

        data = self.data.get(provider, "Pending...")

        if data != "Pending...":
            for arg in args:
                if arg in data:
                    data = data[arg]
                    continue

                data = "N/A"
                break

        return data

    # =========================================================================

    def get_button(self, name: str) -> Optional[discord.ui.Button]:
        """Get view button"""

        for button in self.children:  # type: ignore
            if (button.label == name) or (  # type: ignore
                    button.emoji and button.emoji.name == name  # type: ignore
            ):  # type: ignore
                return button

        return None

    # =========================================================================

    async def change_page(
            self, new_page: int, interaction: discord.Interaction
    ):
        """Change current page"""
        self.__page = new_page

        await self.edit()
        await interaction.response.defer()

    # =========================================================================
    # =========================================================================

    async def update(self, result: Tuple[str, dict]):
        """Update embed"""

        name, data = result

        self.data[name] = data
        for embed in self.embeds:
            embed.update(self)

        await self.edit()

    # =========================================================================

    async def send(self):
        """Send selected embed"""

        if data := await self.ctx.bot.redis.get(self.__cache_key):
            self.data = json.loads(data)
        else:
            await self.__run_batch(
                get_base_providers(self.__config, self.data))
            await self.__run_batch(
                get_auxiliary_providers(self.__config, self.data)
            )
            await self.cache()

        bgp_button = self.get_button("BGP toolkit")
        bgp_button.disabled = False
        bgp_button.url = "https://ipinfo.io/" + self.get_data("ip")

        ipinfo_button = self.get_button("ipinfo.io")
        ipinfo_button.disabled = False
        ipinfo_button.url = (
                "https://bgp.he.net/AS"
                + self.get_data("ipwhois", "asn")
        )

        await self.edit()

    # =========================================================================

    async def edit(self):
        """Edit sent message"""
        embeds = [e.rebuild() for e in self.embeds]
        embed = embeds[self.__page]

        if self.__message:
            await self.__message.edit(
                embed=embed,
                view=self
            )
            return

        self.__message = await self.ctx.send(embed=embed, view=self)

    # =========================================================================

    async def cache(self):
        """Cache result"""
        await self.ctx.bot.redis.set(
            self.__cache_key,
            json.dumps(self.data),
            ex=3600 * 24
        )

    # =========================================================================

    async def delete(self):
        """Delete controller"""
        self.stop()
        await self.__message.delete()
