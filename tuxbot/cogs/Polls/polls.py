import json
import logging
from typing import Dict

import discord
from discord.ext import commands
from yarl import URL

from tuxbot.core.utils.functions.extra import ContextPlus, group_extra
from tuxbot.core.utils.functions.utils import upper_first
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from .functions import emotes as utils_emotes, listeners
from .functions.converters import NewPropositionConvertor, PollConverter
from .models import Poll
from .models.suggests import Suggest

log = logging.getLogger("tuxbot.cogs.Polls")
_ = Translator("Polls", __file__)


class Polls(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        await listeners.cog_command_error(self, ctx, error)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pld: discord.RawReactionActionEvent):
        await listeners.on_raw_reaction_add(self, pld)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, pld: discord.RawReactionActionEvent
    ):
        await listeners.on_raw_reaction_remove(self, pld)

    # =========================================================================
    # =========================================================================

    async def create_poll(
        self,
        ctx: ContextPlus,
        question: str,
        answers: list[str],
        anonymous=False,
    ):
        emotes = utils_emotes.get(len(answers))

        stmt = await ctx.send(
            _(
                "**Preparation**",
                ctx,
                self.bot.config,
            )
        )

        poll_row = await Poll()

        poll_row.channel_id = stmt.channel.id
        poll_row.message_id = stmt.id
        poll_row.author_id = ctx.author.id
        poll_row.content = {}  # type: ignore
        poll_row.is_anonymous = anonymous
        poll_row.available_choices = len(answers)  # type: ignore

        await poll_row.save()

        e = discord.Embed(description=f"**{question}**")
        e.set_author(
            name=ctx.author,
            icon_url="https://img.icons8.com/plasticine/100/000000/survey.png",
        )
        for i, answer in enumerate(answers):
            e.add_field(
                name=f"__{emotes[i]} - {upper_first(answer)}__",
                value="**0** vote",
            )
        e.set_footer(text=f"ID: #{poll_row.id}")

        poll_row.content = e.to_dict()
        await poll_row.save()

        await stmt.edit(content="", embed=e)
        for emote in range(len(answers)):
            await stmt.add_reaction(emotes[emote])

    async def get_poll(
        self, pld: discord.RawReactionActionEvent
    ) -> bool | Poll:
        if pld.user_id != self.bot.user.id:
            poll = await Poll.get_or_none(message_id=pld.message_id)

            if poll is not None:
                emotes = utils_emotes.get(poll.available_choices)

                if pld.emoji.name in emotes:
                    return poll

        return False

    async def update_poll(self, poll: Poll):
        channel: discord.TextChannel = self.bot.get_channel(poll.channel_id)
        message: discord.Message = await channel.fetch_message(poll.message_id)

        chart_base_url = "https://quickchart.io/chart?backgroundColor=white&c="
        chart_options = {
            "type": "pie",
            "data": {"labels": [], "datasets": [{"data": []}]},
        }

        content = (
            json.loads(poll.content)  # type: ignore
            if isinstance(poll.content, str)
            else poll.content
        )

        responses: Dict[int, int] = {}

        async for response in poll.choices:
            if responses.get(response.choice):
                responses[response.choice] += 1
            else:
                responses[response.choice] = 1

        for i, field in enumerate(content.get("fields")):  # type: ignore
            responders = responses.get(i, 0)

            chart_options["data"]["labels"].append(  # type: ignore
                field["name"][6:].replace("__", "")
            )

            chart_options["data"]["datasets"][0]["data"].append(responders)  # type: ignore

            if responders <= 1:
                field["value"] = f"**{responders}** vote"
            else:
                field["value"] = f"**{responders}** votes"

        e = discord.Embed(description=content.get("description"))
        e.set_author(
            name=content.get("author").get("name"),  # type: ignore
            icon_url=content.get("author").get("icon_url"),  # type: ignore
        )
        chart_url = URL(chart_base_url + json.dumps(chart_options))
        e.set_thumbnail(url=str(chart_url))

        for field in content.get("fields"):  # type: ignore
            e.add_field(
                name=field.get("name"), value=field.get("value"), inline=True
            )

        e.set_footer(text=content.get("footer").get("text"))  # type: ignore

        await message.edit(embed=e)

        poll.content = json.dumps(content)  # type: ignore

        await poll.save()

    async def remove_reaction(self, pld: discord.RawReactionActionEvent):
        channel: discord.TextChannel = self.bot.get_channel(pld.channel_id)
        message: discord.Message = await channel.fetch_message(pld.message_id)
        user: discord.User = await self.bot.fetch_user(pld.user_id)

        await message.remove_reaction(pld.emoji.name, user)

    async def created_suggest(
        self, ctx: ContextPlus, poll: PollConverter, new: str
    ):
        stmt = await ctx.send(
            _(
                "**Preparation**",
                ctx,
                self.bot.config,
            )
        )

        suggest_row = await Suggest()

        suggest_row.channel_id = ctx.channel.id
        suggest_row.message_id = stmt.id
        suggest_row.author_id = ctx.author.id

        if isinstance(poll, Poll):
            # pylint: disable=pointless-string-statement
            """Just to change type for PyCharm"""

        suggest_row.poll = poll
        suggest_row.proposition = new  # type: ignore

        await suggest_row.save()

        poll_channel: discord.TextChannel = await self.bot.fetch_channel(
            poll.channel_id
        )
        poll_message = await poll_channel.fetch_message(poll.message_id)

        e = discord.Embed(
            title=_(
                "Proposed addition for poll #{id}", ctx, self.bot.config
            ).format(id=poll.id),
            description=new,
        )
        e.add_field(
            name=_("Poll", ctx, self.bot.config),
            value="[{}]({})".format(
                _("here", ctx, self.bot.config), poll_message.jump_url
            ),
        )
        e.set_footer(
            text=_("Requested by {author}", ctx, self.bot.config).format(
                author=ctx.author.name
            ),
            icon_url=ctx.author.avatar.url,
        )

        await stmt.edit(content="", embed=e)

        for emote in utils_emotes.check:
            await stmt.add_reaction(emote)

    async def get_suggest(
        self, pld: discord.RawReactionActionEvent
    ) -> bool | Suggest:
        if pld.user_id != self.bot.user.id:
            suggest = await Suggest.get_or_none(message_id=pld.message_id)

            if suggest is not None and pld.emoji.name in utils_emotes.check:
                return suggest

        return False

    # =========================================================================
    # =========================================================================

    @group_extra(name="polls", aliases=["poll", "sondages", "sondage"])
    async def _poll(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("poll")

    @_poll.command(name="create", aliases=["new", "nouveau"])
    async def _poll_create(self, ctx: ContextPlus, *, poll: str):
        args: list = poll.split()
        is_anonymous = False

        if "--anonymous" in map(str.lower, args):
            is_anonymous = True
            args.remove("--anonymous")
        elif "--anonyme" in map(str.lower, args):
            is_anonymous = True
            args.remove("--anonyme")

        if args[-1] != "|":
            args.append("|")

        delimiters = [i for i, val in enumerate(args) if val == "|"]

        question = upper_first(" ".join(args[: delimiters[0]]))
        answers = []

        for i in range(len(delimiters) - 1):
            start = delimiters[i] + 1
            end = delimiters[i + 1]

            answers.append(upper_first(" ".join(args[start:end])))

        await self.create_poll(ctx, question, answers, anonymous=is_anonymous)

    @_poll.command(name="propose", aliases=["suggest", "ajout"])
    async def _poll_propose(
        self,
        ctx: ContextPlus,
        poll: PollConverter,
        *,
        new: NewPropositionConvertor,
    ):
        await self.created_suggest(ctx, poll, str(new))
