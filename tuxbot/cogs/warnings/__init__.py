from .warnings import Warnings
from ...core.bot import Tux


def setup(bot: Tux):
    bot.add_cog(Warnings(bot))
