"""
tuxbot.cogs.Polls.commands.poll.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage polls
"""
import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .models.Choices import ChoicesModel
from .models.Polls import PollsModel


@app_commands.guild_only()
class PollCommand(commands.GroupCog, name="poll"):  # type: ignore
    """Manage polls"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        super().__init__()

    # =========================================================================

    @staticmethod
    async def __create_poll(
        channel_id: int,
        message_id: int,
        author_id: int,
        message: str,
        choices: list[str],
    ) -> PollsModel:
        poll = await PollsModel.create(
            channel_id=channel_id,
            message_id=message_id,
            author_id=author_id,
            message=message,
        )

        for choice in choices:
            await ChoicesModel.create(poll=poll, choice=choice)

        return poll

    # =========================================================================

    async def __build_embed(self, poll: PollsModel) -> discord.Embed:
        e = discord.Embed(description=f"**{poll.message}**")

        e.set_author(
            name=await self.bot.fetch_user_or_none(poll.author_id)
            or "Anonymous",
            icon_url="https://img.icons8.com/plasticine/100/000000/survey.png",
        )

        for i, choice in enumerate(await poll.choices.all()):
            e.add_field(
                name=f"__{self.bot.utils.emotes[i]} - {choice.choice}__",
                value=f"**{choice.checked}** "
                f"{'votes' if choice.checked > 1 else 'vote'}",
            )

        e.set_footer(text=f"ID: #{poll.id}")

        return e

    # =========================================================================
    # =========================================================================

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Whenever this command raise an error"""

        if isinstance(error, app_commands.CheckFailure):
            return

        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        self.bot.logger.error(error)

    # =========================================================================
    # =========================================================================

    @app_commands.command(name="create", description="Create a poll")
    async def _poll_create(
        self,
        interaction: discord.Interaction,
        message: str,
        choice1: str,
        choice2: str,
        choice3: str | None = None,
        choice4: str | None = None,
        choice5: str | None = None,
        choice6: str | None = None,
        choice7: str | None = None,
        choice8: str | None = None,
        choice9: str | None = None,
        choice10: str | None = None,
    ) -> None:
        choices = [
            c
            for c in (
                choice1,
                choice2,
                choice3,
                choice4,
                choice5,
                choice6,
                choice7,
                choice8,
                choice9,
                choice10,
            )
            if c
        ]

        stmt: discord.Message = await interaction.channel.send(
            "**Preparing...**"
        )

        poll = await self.__create_poll(
            channel_id=interaction.channel.id,
            message_id=stmt.id,
            author_id=interaction.user.id,
            message=discord.utils.escape_mentions(message),
            choices=choices,
        )

        await stmt.edit(content="", embed=await self.__build_embed(poll))

        for i in range(len(choices)):
            await stmt.add_reaction(self.bot.utils.emotes[i])

        await interaction.response.send_message("created", ephemeral=True)
