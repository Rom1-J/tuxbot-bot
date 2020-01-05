from discord.ext import commands


class commandsPlus(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get("category", 'other')
        self.help = kwargs.get("help", 'No Help Provided')
        self.usage = kwargs.get("usage", 'No Usage Provided')


def commandExtra(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=commandsPlus)


class GroupPlus(commands.Group):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get("category", 'other')
        self.help = kwargs.get("help", 'No Help Provided')
        self.usage = kwargs.get("usage", 'No Usage Provided')


def groupExtra(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=GroupPlus)
