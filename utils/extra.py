from discord.ext import commands


class commandsPlus(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get("category", 'other')


def commandExtra(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=commandsPlus)


class GroupPlus(commands.Group):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get("category", 'other')


def groupExtra(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=GroupPlus)
