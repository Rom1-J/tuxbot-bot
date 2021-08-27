from discord.ext import commands
from discord.ext.commands import Context

from tuxbot.cogs.Tags.functions.exceptions import (
    UnknownTagException,
    ExistingTagException,
    TooLongTagException,
    ReservedTagException,
)
from tuxbot.cogs.Tags.models import Tag


def _(x):
    return x


class TagConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        arg = argument.lower()

        tag_row = await Tag.get_or_none(server_id=ctx.guild.id, name=arg)

        if not tag_row:
            raise UnknownTagException(_("Unknown tag"))

        return arg


class NewTagConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if (tag := ctx.bot.get_command("tag")) is None:
            raise commands.CommandNotFound()

        arg = argument.lower()

        if len(arg) > 50:
            raise TooLongTagException(
                _("Tag must be lower than 50 characters")
            )

        # noinspection PyUnresolvedReferences
        if arg.split(" ")[0] in tag.all_commands:
            raise ReservedTagException(
                _("This tag name starts with a tag subcommand name")
            )

        tag_row = await Tag.get_or_none(server_id=ctx.guild.id, name=arg)

        if tag_row:
            raise ExistingTagException(_("Tag already exists"))

        return arg
