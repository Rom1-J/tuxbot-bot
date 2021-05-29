import logging
import random
import string

import discord
from discord.enums import ButtonStyle
from discord import ui, SelectOption
from discord.ext import commands

from tuxbot.cogs.Dev.functions.utils import TicTacToe
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils import checks
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.Dev")
_ = Translator("Dev", __file__)


class Test(ui.View):
    @ui.button(label="label1", disabled=True, style=ButtonStyle.grey)
    async def label1(self, button, interaction):
        print("label1")

        print(type(button), button)
        print(type(interaction), interaction)

    @ui.button(label="label2", style=ButtonStyle.danger)
    async def label2(self, button, interaction):
        print("label2")

        print(type(button), button)
        print(type(interaction), interaction)


class Test2(ui.View):
    @ui.select(
        placeholder="placeholder",
        min_values=1,
        max_values=3,
        options=[
            SelectOption(
                label="label1",
                value="value1",
                description="description1",
            ),
            SelectOption(
                label="label2",
                value="value2",
                description="description2",
            ),
            SelectOption(
                label="label3",
                value="value3",
                description="description3",
            ),
            SelectOption(
                label="label4",
                value="value4",
                description="description4",
            ),
        ],
    )
    async def select1(self, *args, **kwargs):
        print("select1")

        print(args)
        print(kwargs)


class Dev(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

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
        button = ui.Button(
            style=ButtonStyle.primary,
            label="test",
        )
        button2 = ui.Button(
            style=ButtonStyle.secondary,
            label="test2",
        )
        button3 = ui.Button(
            style=ButtonStyle.green,
            label="test3",
        )
        button4 = ui.Button(
            style=ButtonStyle.blurple,
            label="test4",
        )
        button5 = ui.Button(
            style=ButtonStyle.danger,
            label="test5",
        )

        view = ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)

        await ctx.send("test", view=view)

    # =========================================================================

    @command_extra(name="test2", deletable=True)
    @checks.is_owner()
    async def _test2(self, ctx: ContextPlus):
        await ctx.send(view=Test2())

    # =========================================================================

    @command_extra(name="test3", deletable=False)
    async def _test3(self, ctx: ContextPlus, opponent: discord.Member):
        game = await ctx.send(f"Turn: {ctx.author}")
        game_id = "".join(random.choices(string.ascii_letters, k=10))

        view = TicTacToe(ctx.message.author, opponent, game, game_id=game_id)

        await game.edit(content=f"Turn: {ctx.author}", view=view)
