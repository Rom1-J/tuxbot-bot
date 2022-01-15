"""
tuxbot.cogs.Admin
~~~~~~~~~~~~~~~~~~

Set of owner only command.
"""

from collections import namedtuple


from tuxbot.cogs.Admin.commands.RestartCommand import RestartCommand
from tuxbot.cogs.Admin.commands.UpdateCommand import UpdateCommand

# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
from discord.ext import commands


STANDARD_COMMANDS = (RestartCommand, UpdateCommand)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Admin(*STANDARD_COMMANDS):
    """Set of owner only commands."""

    async def cog_check(self, ctx: commands.Context):
        """Ensure author is owner"""

        if not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner()

        return True

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
