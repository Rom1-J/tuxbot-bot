"""
Tuxbot abstract class module: ModuleABC

Contains all Module properties
"""
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class ModuleABC(commands.Cog):
    """Module Abstract Class"""
    bot: Tuxbot

    def crash_report(self) -> str:
        """Generate crash report"""
        report = f"{'='*10}{self.__class__.__name__}{'='*10}"

        report += "\nhas models:"
        if hasattr(self, "models") and (models := self.models):
            report += str(models)
        else:
            report += "No"

        report += "\nhas config:"
        if hasattr(self, "config") and (config := self.config):
            report += str(config)
        else:
            report += "No"

        report += "\nhas commands:"
        report += str([c.name for c in self.get_commands()])

        return report
