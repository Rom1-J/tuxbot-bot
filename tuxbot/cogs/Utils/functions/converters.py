from discord.ext import commands
from discord.ext.commands import Context

from tuxbot.cogs.Utils.functions.exceptions import UserNotFound


def _(x):
    return x


class QuoteMessage:
    content: str
    author: str


class QuoteConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        try:
            return await commands.MessageConverter().convert(ctx, argument)
        except commands.BadArgument:
            message = QuoteMessage()

            message.content = argument
            message.author = str(ctx.message.author)

            return message


class UserOrMeConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if argument:
            try:
                return await commands.MemberConverter().convert(ctx, argument)
            except commands.MemberNotFound:
                pass

            try:
                return await commands.UserConverter().convert(ctx, argument)
            except commands.UserNotFound:
                pass

            # todo: find why this does not work
            raise UserNotFound(_("Unable to find this user"))

        return ctx.author
