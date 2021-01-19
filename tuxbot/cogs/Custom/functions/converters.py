from discord.ext import commands
from jishaku.models import copy_context_with


_ = lambda x: x


class AliasConvertor(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.split(" | ")

        if len(args) <= 1:
            raise commands.BadArgument(
                _("Alias must be like `[command] | [alias]`")
            )

        command_ctx = await copy_context_with(
            ctx, content=ctx.prefix + args[0]
        )
        alias_ctx = await copy_context_with(ctx, content=ctx.prefix + args[1])

        if command_ctx.command is None:
            raise commands.BadArgument(_("Unknown command"))

        if args[0] != args[1] and alias_ctx.command is not None:
            raise commands.BadArgument(_("Command already exists"))

        return argument
