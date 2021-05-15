from discord.ext import commands


class TagsException(commands.BadArgument):
    pass


class UnknownTagException(TagsException):
    pass


class ExistingTagException(TagsException):
    pass
