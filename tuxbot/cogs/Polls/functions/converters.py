from discord.ext import commands
from tuxbot.cogs.Polls.functions.exceptions import (
    TooLongProposition,
    InvalidChannel,
    BadPoll,
)
from tuxbot.cogs.Polls.models import Poll


def _(x):
    return x


class PollConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            poll = await commands.MessageConverter().convert(ctx, argument)

            if poll.channel.id != ctx.channel.id:
                raise InvalidChannel(
                    _("Please provide a message in this channel")
                )

            if (
                poll.author.id != ctx.bot.user.id
                or len(poll.embeds) != 1
                or poll.embeds[0].to_dict().get("footer", {}).get("text", None)
                is None
            ):
                raise BadPoll(_("Unable to find this poll"))

            poll_id = poll.embeds[0].to_dict().get("footer").get("text")
            poll_id = poll_id.replace("ID: #", "")

            if not poll_id.isdigit():
                raise BadPoll(_("Unable to find this poll"))
        except commands.BadArgument:
            poll_id = str(argument).replace("ID:", "").replace("#", "")

            if not poll_id.isdigit():
                raise BadPoll(_("Unable to find this poll"))

        poll = await Poll.get_or_none(id=int(poll_id))

        if poll.channel_id != ctx.channel.id:
            raise InvalidChannel(_("Please provide a message in this channel"))

        if poll is None:
            raise BadPoll(_("Unable to find this poll"))

        return poll


class NewPropositionConvertor(commands.Converter):
    async def convert(self, ctx, argument):  # skipcq: PYL-W0613
        if len(argument) > 30:
            raise TooLongProposition(
                _("Your proposal must be smaller than 30")
            )

        return argument
