from discord.ext import commands


class VocalException(commands.BadArgument):
    pass


class EmptyChannelException(VocalException):
    pass


class NoDMException(VocalException):
    pass


class IncorrectChannelException(VocalException):
    pass


class TrackTooLong(VocalException):
    pass
