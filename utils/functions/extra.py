from discord.ext import commands
from utils import Config


class CommandsPlus(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get("category", 'other')


class GroupPlus(commands.Group):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get("category", 'other')


class ContextPlus(commands.Context):
    async def send(self, **kwargs):
        config = Config('./configs/config.cfg')
        content = kwargs.pop('content')

        content = content.replace(config.get("bot", "Token"), 'Whoops! leaked token')
        content = content.replace(config.get("webhook", "Token"), 'Whoops! leaked token')

        kwargs['content'] = content

        return await super().send(**kwargs)


def commandExtra(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=CommandsPlus)


def groupExtra(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=GroupPlus)
