from .network import Network
from ...core.bot import Tux


def setup(bot: Tux):
    bot.add_cog(Network(bot))
