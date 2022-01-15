from discord.ext import commands


class TagsException(commands.BadArgument):
    pass


class UnknownTagException(TagsException):
    pass


class ExistingTagException(TagsException):
    pass


class TooLongTagException(TagsException):
    pass


class ReservedTagException(TagsException):
    pass
