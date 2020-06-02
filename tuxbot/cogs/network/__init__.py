from .network import Network


def setup(bot):
    bot.add_cog(Network(bot))
