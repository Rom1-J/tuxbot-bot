import copy
from typing import List, Optional, Union, Dict, TYPE_CHECKING

import discord
from discord.ext import commands

from .buttons import ButtonType
from .embeds import Embeds
from .panels import ViewPanel


if TYPE_CHECKING:
    Author = Union[discord.User, discord.Member]


class ViewController(discord.ui.View):
    children: List[ButtonType]  # type: ignore
    page: str = "global"
    pages: tuple = ("global", "geo", "raw")
    sent_message = None

    embeds: Dict[str, discord.Embed] = {}

    def __init__(
        self,
        ctx: commands.Context,
        author: "Author",
        data: dict,
    ):
        super().__init__(timeout=60)

        self.author: Author = author

        self.ctx = ctx
        self.data = data

        panel = ViewPanel.buttons

        for x, row in enumerate(panel):
            for button in row:
                self.add_item(button(row=x, controller=self))

    # =========================================================================
    # =========================================================================

    async def on_timeout(self) -> None:
        self.clear_items()

        await self.send()

    # =========================================================================

    async def send(self, interaction: Optional[discord.Interaction] = None):
        embed = await self.select_embed()

        args = {"embed": embed}

        if interaction:
            if (interaction.user == self.author) and self.sent_message:
                self.sent_message = await self.sent_message.edit(
                    **args, view=self
                )
                return

            ephemeral_view = copy.copy(self)

            if button := ephemeral_view.get_button("delete"):
                self.remove_item(button)

            return await interaction.response.send_message(
                **args, view=self, ephemeral=True  # type: ignore
            )

        if self.sent_message is None:
            self.sent_message = await self.ctx.send(**args, view=self)
        else:
            self.sent_message = await self.sent_message.edit(
                content="", **args, view=self
            )

    # =========================================================================
    # =========================================================================

    async def select_embed(self) -> Optional[discord.Embed]:
        self.embeds = await self.build_embeds()
        return self.embeds[self.page]

    # =========================================================================

    async def build_embeds(self) -> Dict[str, discord.Embed]:
        embeds = Embeds(self)

        output = {}

        for page_name in self.pages:
            embed = await embeds.__getattribute__(f"{page_name}_embed")()

            output[page_name] = embed

        return output

    # =========================================================================

    async def change_to(self, page: str, interaction: discord.Interaction):
        self.page = page

        for page_name in self.pages:
            if button := self.get_button(page_name):
                button.disabled = False

        if current_button := self.get_button(page):
            current_button.disabled = True

        await self.send(interaction)

    # =========================================================================

    def get_button(self, name: str) -> Optional[discord.ui.Button]:
        for button in self.children:  # type: ignore
            if (button.label == name) or (  # type: ignore
                button.emoji and button.emoji.name == name  # type: ignore
            ):  # type: ignore
                return button

        return None
