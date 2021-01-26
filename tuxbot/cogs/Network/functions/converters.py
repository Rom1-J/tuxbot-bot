import re

from discord.ext import commands

from tuxbot.cogs.Network.functions.exceptions import (
    InvalidIp,
    InvalidDomain,
    InvalidQueryType,
)


def _(x):
    return x


DOMAIN_PATTERN = r"^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$"
IPV4_PATTERN = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
IPV6_PATTERN = r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"


class IPConverter(commands.Converter):
    async def convert(self, ctx, argument):  # skipcq: PYL-W0613
        argument = argument.replace("http://", "").replace("https://", "")

        check_domain = re.match(DOMAIN_PATTERN, argument)
        check_ipv4 = re.match(IPV4_PATTERN, argument)
        check_ipv6 = re.match(IPV6_PATTERN, argument)

        if check_domain or check_ipv4 or check_ipv6:
            return argument

        raise InvalidIp(_("Invalid ip or domain"))


class IPCheckerConverter(commands.Converter):
    async def convert(self, ctx, argument):  # skipcq: PYL-W0613
        if not argument.startswith("http"):
            return f"http://{argument}"

        return argument


class DomainCheckerConverter(commands.Converter):
    async def convert(self, ctx, argument):  # skipcq: PYL-W0613
        argument = argument.replace("http://", "").replace("https://", "")

        check_domain = re.match(DOMAIN_PATTERN, argument)

        if check_domain:
            return argument

        raise InvalidDomain(_("Invalid domain"))


class QueryTypeConverter(commands.Converter):
    async def convert(self, ctx, argument):  # skipcq: PYL-W0613
        argument = argument.lower()
        query_types = [
            "a",
            "aaaa",
            "cname",
            "ns",
            "ds",
            "dnskey",
            "soa",
            "txt",
            "ptr",
            "mx",
        ]

        if argument in query_types:
            return argument

        raise InvalidQueryType(
            _(
                "Supported queries : A, AAAA, CNAME, NS, DS, DNSKEY, SOA, TXT, PTR, MX"
            )
        )


class IPVersionConverter(commands.Converter):
    async def convert(self, ctx, argument):  # skipcq: PYL-W0613
        if not argument:
            return argument

        argument = argument.replace("-", "").replace("p", "").replace("v", "")

        if argument not in ["4", "6"]:
            raise InvalidIp(_("Invalid ip version"))

        return argument
