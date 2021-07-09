import logging

import discord
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils import checks
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus
from .functions.utils import playlist as pl

log = logging.getLogger("tuxbot.cogs.Test")
_ = Translator("Test", __file__)


def gen_playlist(playlist):
    parts = list(zip(*[iter(playlist)] * 23))
    out = [[]]
    pages = 0
    i = 0

    for part_id, part in enumerate(parts, start=1):
        for song in part:
            out[pages].append(
                discord.SelectOption(
                    value=str(i),
                    label=song["label"],
                    description=song["description"],
                    emoji=song["emoji"],
                )
            )

            i += 1

        if pages > 0:
            out[pages].append(
                discord.SelectOption(value="less", label="less...", emoji="➖")
            )

        if part_id < len(parts):
            out[pages].append(
                discord.SelectOption(value="more", label="More...", emoji="➕")
            )

        pages += 1
        out.append([])

    if not out[-1]:
        del out[-1]

    return out


class PlaylistSelect(discord.ui.Select):
    def __init__(self, options: list):
        self._page = 0
        self._options = options

        super().__init__(
            custom_id="Some identifier",
            placeholder=f"Page: {self._page + 1}/{len(self._options)}",
            min_values=1,
            max_values=1,
            options=self._options[self._page],
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.data["values"][0] == "more":
            self._page += 1
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

        elif interaction.data["values"][0] == "less":
            self._page -= 1
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

        view = discord.ui.View()
        view.add_item(self)
        await interaction.message.edit(view=view)


class Test(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    # =========================================================================
    # =========================================================================

    @command_extra(name="crash", deletable=True)
    @checks.is_owner()
    async def _crash(self, ctx: ContextPlus, crash_type: str):
        if crash_type == "ZeroDivisionError":
            await ctx.send(str(5 / 0))
        elif crash_type == "TypeError":
            # noinspection PyTypeChecker
            await ctx.send(str(int([])))  # type: ignore
        elif crash_type == "IndexError":
            await ctx.send(str([0][5]))

    # =========================================================================

    @command_extra(name="test", deletable=True)
    @checks.is_owner()
    async def _test(self, ctx: ContextPlus):
        view = discord.ui.View()
        view.add_item(PlaylistSelect(gen_playlist(pl)))

        await ctx.send("Choisir une musique:", view=view)

    # =========================================================================
