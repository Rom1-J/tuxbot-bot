import shlex

from discord.ext import commands
from discord.ext.commands import Context

from tuxbot.cogs.Mod.functions.exceptions import (
    RuleTooLongException,
    UnknownRuleException,
    NonMessageException,
    NonBotMessageException,
    ReasonTooLongException,
)
from tuxbot.cogs.Mod.functions.parser import AutoBanParser
from tuxbot.cogs.Mod.models import Rule


def _(x):
    return x


class RuleIDConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if not argument.isdigit():
            raise UnknownRuleException(_("Unknown rule"))

        arg = int(argument)

        rule_row = await Rule.get_or_none(server_id=ctx.guild.id, rule_id=arg)

        if not rule_row:
            raise UnknownRuleException(_("Unknown rule"))

        return arg


class RuleConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if len(argument) > 300:
            raise RuleTooLongException(
                _("Rule length must be 300 characters or lower.")
            )

        return argument


class BotMessageConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        try:
            m = await commands.MessageConverter().convert(ctx, argument)

            if m.author == ctx.me:
                return m

            raise NonBotMessageException(_("Please provide one of my message"))
        except commands.BadArgument:
            raise NonMessageException(
                _("Please provide a message in this guild")
            )


class ReasonConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if argument is None:
            return f"{ctx.author.display_name} (ID: {ctx.author.id})"

        if len(argument) > 300:
            raise ReasonTooLongException(
                _("Reason length must be 300 characters or lower.")
            )

        return argument


class AutoBanConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        parser = AutoBanParser(add_help=False, allow_abbrev=False)
        parser.add_argument(
            "-r", "--reason", type=str, default="Auto ban from bot"
        )
        parser.add_argument("-m", "--match", type=str)
        parser.add_argument("-l", "--log_channel", type=int, default=None)
        parser.add_argument("--delete", action="store_true")

        try:
            return parser.parse_args(shlex.split(argument))
        except Exception:
            return None
