from typing import List, Optional, Dict

import discord
from discord import ui
from discord.enums import ButtonStyle


class TicTacToe(ui.View):
    turn: int = 0
    grid: Dict[str, List[List[Optional[int]]]] = {}
    win: bool = False

    def __init__(self, player: discord.Member, opponent: discord.Member,
                 game: discord.Message, game_id: str):
        super().__init__()

        self.player = player
        self.opponent = opponent
        self.game = game

        self.game_id = game_id

        self.init_grid()

    def init_grid(self):
        self.grid[self.game_id]: List[List[Optional[int]]] = [
            [None for _ in range(3)]
            for _ in range(3)
        ]

    def get_grid(self):
        return self.grid[self.game_id]

    def get_turn(self):
        return self.player if self.turn == 0 else self.opponent

    def get_emoji(self):
        return "❌" if self.turn == 0 else "⭕"

    def check_win(self):
        wins = [
            [self.get_grid()[0][0], self.get_grid()[0][1], self.get_grid()[0][2]],
            [self.get_grid()[1][0], self.get_grid()[1][1], self.get_grid()[1][2]],
            [self.get_grid()[2][0], self.get_grid()[2][1], self.get_grid()[2][2]],
            [self.get_grid()[0][0], self.get_grid()[1][0], self.get_grid()[2][0]],
            [self.get_grid()[0][1], self.get_grid()[1][1], self.get_grid()[2][1]],
            [self.get_grid()[0][2], self.get_grid()[1][2], self.get_grid()[2][2]],
            [self.get_grid()[0][0], self.get_grid()[1][1], self.get_grid()[2][2]],
            [self.get_grid()[2][0], self.get_grid()[1][1], self.get_grid()[0][2]],
        ]

        return [self.turn, self.turn, self.turn] in wins

    async def congrats(self):
        self.win = True
        del self.grid[self.game_id]

        await self.game.edit(
            content=f"{self.get_turn()} wins!",
            view=self
        )

    def set_pos(self, i, j):
        self.get_grid()[i][j] = self.turn

    async def next_turn(self, i, j):
        if self.win:
            return

        self.set_pos(i, j)

        if self.check_win():
            return await self.congrats()

        self.turn = 1 if self.turn == 0 else 0

        await self.game.edit(
            content=f"Turn {self.get_turn()}",
            view=self
        )

    # =========================================================================
    # =========================================================================

    @ui.button(label="•", style=ButtonStyle.grey, group=1)
    async def button_1(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(0, 0)

    @ui.button(label="•", style=ButtonStyle.grey, group=1)
    async def button_2(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(0, 1)

    @ui.button(label="•", style=ButtonStyle.grey, group=1)
    async def button_3(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(0, 2)

    # =========================================================================
    # =========================================================================

    @ui.button(label="•", style=ButtonStyle.grey, group=2)
    async def button_4(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(1, 0)

    @ui.button(label="•", style=ButtonStyle.grey, group=2)
    async def button_5(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(1, 1)

    @ui.button(label="•", style=ButtonStyle.grey, group=2)
    async def button_6(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(1, 2)

    # =========================================================================
    # =========================================================================

    @ui.button(label="•", style=ButtonStyle.grey, group=3)
    async def button_7(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(2, 0)

    @ui.button(label="•", style=ButtonStyle.grey, group=3)
    async def button_8(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(2, 1)

    @ui.button(label="•", style=ButtonStyle.grey, group=3)
    async def button_9(self, button: ui.Button,
                       interaction: discord.Interaction):
        if button.label == "•" and interaction.user == self.get_turn():
            button.label = ""
            button.emoji = self.get_emoji()
            await self.next_turn(2, 2)
