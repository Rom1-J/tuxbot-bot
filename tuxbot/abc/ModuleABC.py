"""
Tuxbot abstract class module: ModuleABC

Contains all Module properties
"""
import typing

from discord.ext import commands
from tortoise.models import ModelMeta

from tuxbot.core.Tuxbot import Tuxbot


class ModuleABC(commands.Cog):
    """Module Abstract Class"""

    bot: Tuxbot
    models: ModelMeta
    config: dict[str, typing.Any]

    def crash_report(self) -> str:
        """Generate crash report"""
        report = f"{'='*10}{self.__class__.__name__}{'='*10}"

        report += "\nhas models:"
        # pylint: disable=no-member
        if hasattr(self, "models") and (models := self.models):
            report += str(models)
        else:
            report += "No"

        report += "\nhas config:"
        # pylint: disable=no-member
        if hasattr(self, "config") and (config := self.config):
            report += str(config)
        else:
            report += "No"

        report += "\nhas commands:"
        report += str([c.name for c in self.get_commands()])

        return report
