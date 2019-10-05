import re

import aiohttp
import discord
from discord.ext import commands
from bot import TuxBot
import socket
from socket import AF_INET6

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

        try:
            if ip_type in ('v6', 'ipv6'):
                try:
                    ip = socket.getaddrinfo(addr, None, AF_INET6)[1][4][0]
                except socket.gaierror:
                    return await ctx.send(
                        Texts('utility', ctx).get('ipv6 not available'))
            else:
                ip = socket.gethostbyname(addr)

            async with self.bot.session.get(f"http://ip-api.com/json/{ip}") \
                    as s:
                response: dict = await s.json()

                if response.get('status') == 'success':
                    e = discord.Embed(
                        title=f"{Texts('utility', ctx).get('Information for')}"
                              f" ``{addr}`` *`({response.get('query')})`*",
                        color=0x5858d7
                    )

                    e.add_field(
                        name=Texts('utility', ctx).get('Belongs to :'),
                        value=response.get('org', 'N/A'),
                        inline=False
                    )

                    e.add_field(
                        name=Texts('utility', ctx).get('Is located at :'),
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
                        content=f"{Texts('utility', ctx).get('info not available')}"
                                f"``{response.get('query')}``")

        except Exception:
            await ctx.send(
                f"{Texts('utility', ctx).get('Cannot connect to host')} {addr}"
            )

    """---------------------------------------------------------------------"""

    @commands.command(name='getheaders')
    async def _getheaders(self, ctx: commands.Context, addr: str):
        if (addr.startswith('http') or addr.startswith('ftp')) is not True:
            addr = f"http://{addr}"

        await ctx.trigger_typing()

        try:
            async with self.bot.session.get(addr) as s:
                e = discord.Embed(
                    title=f"{Texts('utility', ctx).get('Headers of')} {addr}",
                    color=0xd75858
                )
                e.add_field(name="Status", value=s.status, inline=True)
                e.set_thumbnail(url=f"https://http.cat/{s.status}")

                headers = dict(s.headers.items())
                headers.pop('Set-Cookie', headers)

                for key, value in headers.items():
                    e.add_field(name=key, value=value, inline=True)
                await ctx.send(embed=e)

        except aiohttp.client_exceptions.ClientError:
            await ctx.send(
                f"{Texts('utility', ctx).get('Cannot connect to host')} {addr}"
            )

    """---------------------------------------------------------------------"""

    @commands.command(name='git', aliases=['sources', 'source', 'github'])
    async def _git(self, ctx):
        e = discord.Embed(
            title=Texts('utility', ctx).get('git repo'),
            description=Texts('utility', ctx).get('git text'),
            colour=0xE9D460
        )
        e.set_author(
            name='Gnous',
            icon_url="https://cdn.gnous.eu/logo1.png"
        )
        await ctx.send(embed=e)

    """---------------------------------------------------------------------"""

    @commands.command(name='quote')
    async def _quote(self, ctx, message_id: discord.Message):
        e = discord.Embed(
            colour=message_id.author.colour,
            description=message_id.clean_content,
            timestamp=message_id.created_at
        )
        e.set_author(
            name=message_id.author.display_name,
            icon_url=message_id.author.avatar_url_as(format="jpg")
        )
        if len(message_id.attachments) >= 1:
            e.set_image(url=message_id.attachments[0].url)

        e.add_field(name="**Original**",
                    value=f"[Go!]({message_id.jump_url})")
        e.set_footer(text="#" + message_id.channel.name)

        await ctx.send(embed=e)


def setup(bot: TuxBot):
    bot.add_cog(Utility(bot))
