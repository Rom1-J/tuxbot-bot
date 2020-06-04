from .images import Images
from ...core.bot import Tux


def setup(bot: Tux):
    bot.add_cog(Images(bot))
