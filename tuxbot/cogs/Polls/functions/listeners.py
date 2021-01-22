import json
from os.path import dirname

import discord
from tuxbot.cogs import Polls

from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.utils import upper_first
from . import emotes as utils_emotes
from .exceptions import InvalidChannel, BadPoll, TooLongProposition
from ..models import Response, Poll, Suggest

_ = Translator("Polls", dirname(__file__))


async def _poll_reaction_add(
    self: Polls, pld: discord.RawReactionActionEvent, poll: Poll
):
    if poll.is_anonymous:
        try:
            await self.remove_reaction(pld)
        except discord.errors.Forbidden:
            pass
    choice = utils_emotes.get_index(pld.emoji.name)

    response = await Response.get_or_none(
        user_id=pld.user_id, choice=choice, poll__id=poll.id
    )

    if response is not None:
        await poll.choices.remove(response)
        await response.delete()
    else:
        res = await Response.create(
            user_id=pld.user_id, poll=poll, choice=choice
        )
        await poll.choices.add(res)

    await self.update_poll(poll)


async def _suggest_reaction_add(
    self: Polls, pld: discord.RawReactionActionEvent, suggest: Suggest
):
    poll = await suggest.poll

    if (
        poll.author_id == pld.user_id
        or (await self.bot.is_owner(discord.Object(pld.user_id)))
        or (
            (channel := await self.bot.fetch_channel(pld.channel_id))
            .permissions_for(await channel.guild.fetch_member(pld.user_id))
            .administrator
        )
    ):

        if pld.emoji.name == utils_emotes.check[0]:
            poll.available_choices += 1

            emote = utils_emotes.emotes[poll.available_choices - 1]

            content = (
                json.loads(poll.content)
                if isinstance(poll.content, str)
                else poll.content
            )

            content["fields"].append(
                {
                    "name": f"__{emote} - {upper_first(suggest.proposition)}__",
                    "value": "**0** vote",
                }
            )

            await poll.save()

            channel: discord.TextChannel = await self.bot.fetch_channel(
                poll.channel_id
            )
            message = await channel.fetch_message(poll.message_id)

            await message.add_reaction(emote)

            await self.update_poll(poll)

        channel: discord.TextChannel = await self.bot.fetch_channel(
            suggest.channel_id
        )
        message = await channel.fetch_message(suggest.message_id)

        await message.delete()

        await suggest.delete()

    else:
        try:
            await self.remove_reaction(pld)
        except discord.errors.Forbidden:
            pass


async def cog_command_error(self: Polls, ctx, error):
    if isinstance(error, (InvalidChannel, BadPoll, TooLongProposition)):
        await ctx.send(_(str(error), ctx, self.bot.config))


async def on_raw_reaction_add(
    self: Polls, pld: discord.RawReactionActionEvent
):
    poll = await self.get_poll(pld)

    if poll:
        await _poll_reaction_add(self, pld, poll)

    elif suggest := await self.get_suggest(pld):
        await _suggest_reaction_add(self, pld, suggest)


async def on_raw_reaction_remove(self, pld: discord.RawReactionActionEvent):
    poll = await self.get_poll(pld)

    if poll:
        choice = utils_emotes.get_index(pld.emoji.name)

        response = await Response.get_or_none(
            user_id=pld.user_id, choice=choice, poll__id=poll.id
        )

        if response is not None:
            await poll.choices.remove(response)
            await response.delete()

        await self.update_poll(poll)
