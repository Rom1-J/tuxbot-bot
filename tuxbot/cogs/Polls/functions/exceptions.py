from discord.ext import commands


class BadPoll(commands.BadArgument):
    pass


class InvalidChannel(commands.BadArgument):
    pass


class TooLongProposition(commands.BadArgument):
    pass
