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


class InetConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if "6" in argument:
            return 6

        if "4" in argument:
            return 4

        return None


class DomainConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if not argument.startswith("http"):
            return f"http://{argument}"

        return argument


class QueryTypeConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        return argument.lower()


class ASConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        return argument.lower().lstrip("as")
