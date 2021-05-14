from discord.ext import commands
from discord.ext.commands import Context

from tuxbot.cogs.Mod.functions.exceptions import (
    RuleTooLongException,
    UnknownRuleException,
)
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
