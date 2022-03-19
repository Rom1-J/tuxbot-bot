from typing import TYPE_CHECKING, List, Union

import discord
from discord.ext import commands

from .buttons import ButtonType
from .panels import ViewPanel

if TYPE_CHECKING:
    Author = Union[discord.User, discord.Member]


class ViewController(discord.ui.View):
    children: List[ButtonType]  # type: ignore

    sent_message = None

    def __init__(
        self,
        ctx: commands.Context,
        data: "Author",
    ):
        super().__init__(timeout=60)

        self.data: Author = data

        self.ctx = ctx

        panel = ViewPanel.buttons

        for x, row in enumerate(panel):
            for button in row:  # type: ignore
                self.add_item(button(row=x, controller=self))

    # =========================================================================
    # =========================================================================

    async def on_timeout(self) -> None:
        """Remove buttons after timeout"""

        self.clear_items()

        await self.send()

    # =========================================================================

    async def send(self):
        """Send selected embed"""

        embed = discord.Embed(
            title=f"Avatar of {self.data}",
            color=self.ctx.bot.utils.colors.EMBED_BORDER.value,
        )
        embed.set_image(url=self.data.display_avatar.url)

        if self.sent_message is None:
            self.sent_message = await self.ctx.send(embed=embed, view=self)
        else:
            self.sent_message = await self.sent_message.edit(
                content="", embed=embed, view=self
            )
