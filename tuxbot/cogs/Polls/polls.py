import logging

from discord.ext import commands

from tuxbot.core.utils.functions.extra import ContextPlus, group_extra
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)

log = logging.getLogger("tuxbot.cogs.Polls")
_ = Translator("Polls", __file__)


class Polls(commands.Cog, name="Polls"):
    def __init__(self, bot: Tux):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @group_extra(name="polls", aliases=["poll", "sondages", "sondage"])
    async def _polls(self, ctx: ContextPlus, *, message):
        if ctx.invoked_subcommand is None:
            args: list = message.lower().split()
            is_anonymous = False

            if "--anonymous" in args:
                is_anonymous = True
                args.remove("--anonymous")
            elif "--anonyme" in args:
                is_anonymous = True
                args.remove("--anonyme")

            if args[-1] != "|":
                args.append("|")

            delimiters = [i for i, val in enumerate(args) if val == "|"]

            question = " ".join(args[0 : delimiters[0]]).capitalize()
            answers = []

            for i in range(len(delimiters) - 1):
                start = delimiters[i] + 1
                end = delimiters[i + 1]

                answers.append(" ".join(args[start:end]).capitalize())

            await ctx.send(
                f"{message=}\n{question=}\n{answers=}\n{is_anonymous=}"
            )
