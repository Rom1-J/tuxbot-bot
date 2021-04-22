from discord.ext import commands
from discord.ext.commands import Context


def _(x):
    return x


class IPConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        argument = argument.replace("http://", "").replace("https://", "")
        argument = argument.rstrip("/")

        if argument.startswith("`") and argument.endswith("`"):
            argument = argument.lstrip("`").rstrip("`")

        return argument.lower()


class DomainConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if not argument.startswith("http"):
            return f"http://{argument}"

        return argument


class QueryTypeConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        return argument.lower()


class IPVersionConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if not argument:
            return argument

        return argument.replace("-", "").replace("ip", "").replace("v", "")


class ASConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        return argument.lower().lstrip("as")
