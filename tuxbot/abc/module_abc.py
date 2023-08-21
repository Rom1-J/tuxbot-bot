"""
Tuxbot abstract class module: ModuleABC.

Contains all Module properties
"""
import typing

from discord.ext import commands
from tortoise.models import ModelMeta


if typing.TYPE_CHECKING:
    from tuxbot.core.tuxbot import Tuxbot


class ModuleABC(commands.Cog):
    """Module Abstract Class."""

    bot: "Tuxbot"
    models: ModelMeta

    def crash_report(self: typing.Self) -> str:
        """Generate crash report."""
        report = f"{'='*10}{self.__class__.__name__}{'='*10}"

        report += "\nhas models:"
        # pylint: disable=no-member
        if hasattr(self, "models") and (models := self.models):
            report += str(models)
        else:
            report += "No"

        report += "\nhas commands:"
        report += str([c.name for c in self.get_commands()])

        return report
