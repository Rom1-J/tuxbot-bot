from discord.ext import commands


class ModException(commands.BadArgument):
    pass


class RuleTooLongException(ModException):
    pass


class UnknownRuleException(ModException):
    pass


class NonMessageException(ModException):
    pass


class NonBotMessageException(ModException):
    pass


class ReasonTooLongException(ModException):
    pass
