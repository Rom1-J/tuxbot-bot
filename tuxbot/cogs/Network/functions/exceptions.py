from discord.ext import commands


class NetworkException(commands.BadArgument):
    pass


class RFC18(NetworkException):
    pass


class InvalidIp(NetworkException):
    pass


class InvalidDomain(NetworkException):
    pass


class InvalidQueryType(NetworkException):
    pass


class VersionNotFound(NetworkException):
    pass
