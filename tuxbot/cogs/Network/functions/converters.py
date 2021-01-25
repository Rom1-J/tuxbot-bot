import re

from discord.ext import commands

from tuxbot.cogs.Network.functions.exceptions import InvalidIp


def _(x):
    return x


DOMAIN_PATTERN = "^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$"
IP_PATTERN = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


class IPConverter(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.replace("http://", "").replace("https://", "")

        check_domain = re.match(DOMAIN_PATTERN, argument)
        check_ip = re.match(IP_PATTERN, argument)

        if check_domain or check_ip:
            return argument

        raise InvalidIp(_("Invalid ip or domain"))


class IPVersionConverter(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument:
            return argument

        argument = argument.replace("-", "").replace("p", "").replace("v", "")

        if argument not in ["4", "6"]:
            raise InvalidIp(_("Invalid ip version"))

        return argument
