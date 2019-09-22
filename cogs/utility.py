import re

import discord
from discord.ext import commands
from bot import TuxBot
import socket

from .utils.lang import Texts


class Utility(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    """---------------------------------------------------------------------"""

    @commands.command(name='iplocalise')
    async def _iplocalise(self, ctx: commands.Context, addr, ip_type=''):
        addr = re.sub(r'http(s?)://', '', addr)
        addr = addr[:-1] if addr.endswith('/') else addr

        await ctx.trigger_typing()

        if ip_type in ('v6', 'ipv6'):
            try:
                ip = socket.getaddrinfo(addr, None, socket.AF_INET6)[1][4][0]
            except socket.gaierror:
                return await ctx.send(
                    Texts('utility').get('ipv6 not available'))
        else:
            ip = socket.gethostbyname(addr)

        async with self.bot.session.get(f"http://ip-api.com/json/{ip}") as s:
            response: dict = await s.json()

            if response.get('status') == 'success':
                e = discord.Embed(
                    title=f"{Texts('utility').get('Information for')} "
                          f"``{addr}`` *`({response.get('query')})`*",
                    color=0x5858d7
                )

                e.add_field(
                    name=Texts('utility').get('Belongs to :'),
                    value=response.get('org', 'N/A'),
                    inline=False
                )

                e.add_field(
                    name=Texts('utility').get('Is located at :'),
                    value=response.get('city', 'N/A'),
                    inline=True
                )

                e.add_field(
                    name="Region :",
                    value=f"{response.get('regionName', 'N/A')} "
                          f"({response.get('country', 'N/A')})",
                    inline=True
                )

                e.set_thumbnail(
                    url=f"https://www.countryflags.io/"
                        f"{response.get('countryCode')}/flat/64.png")

                await ctx.send(embed=e)
            else:
                await ctx.send(
                    content=f"{Texts('utility').get('info not available')}"
                            f"``{response.get('query')}``")


def setup(bot: TuxBot):
    bot.add_cog(Utility(bot))
