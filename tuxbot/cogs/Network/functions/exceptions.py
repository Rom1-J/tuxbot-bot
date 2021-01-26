from discord.ext import commands


class RFC18(commands.UserNotFound):
    pass


class InvalidIp(commands.BadArgument):
    pass


class InvalidDomain(commands.BadArgument):
    pass


class InvalidQueryType(commands.BadArgument):
    pass


class VersionNotFound(commands.BadArgument):
    pass
