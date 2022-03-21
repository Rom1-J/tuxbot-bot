"""
tuxbot.cogs.Network.commands.Getheaders.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows address headers.
"""

import asyncio
import socket
from urllib.parse import urlparse

import aiohttp
import discord
import ipwhois
from discord.ext import commands
from ipwhois import IPWhois

from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import RFC1918
from .exceptions import UnreachableAddress


class GetheadersCommand(commands.Cog):
    """Shows address headers"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __check_for_rfc1918_or_raise(ip: str) -> None:
        """Check for RFC1918 or raise"""

        def _check_for_rfc1918_or_raise(_ip: str) -> None:
            try:
                IPWhois(
                    socket.getaddrinfo(urlparse(_ip).netloc, None)[1][4][0]
                ).lookup_whois()
            except ipwhois.exceptions.IPDefinedError as e:
                raise RFC1918(
                    "This IP address defined as Private-Use Networks "
                    "via RFC 1918."
                ) from e

        try:
            return await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _check_for_rfc1918_or_raise, str(ip)  # type: ignore
                ),
                timeout=2,
            )
        except (asyncio.exceptions.TimeoutError, socket.gaierror):
            raise UnreachableAddress("Failed to reach this address.")

    # =========================================================================

    @staticmethod
    async def __get_headers(ip: str, user_agent: str) -> tuple:
        """Retrieve address headers"""

        req_headers = {}

        if user_agent:
            req_headers["User-Agent"] = user_agent

        async with aiohttp.ClientSession() as cs, cs.get(
            str(ip),
            headers=req_headers,
            timeout=aiohttp.ClientTimeout(total=8),
        ) as s:
            # noinspection PyTypeChecker
            headers = dict(s.headers.items())
            headers.pop("Set-Cookie", headers)
            headers.pop("X-Client-IP", headers)

            return s, headers

    # =========================================================================
    # =========================================================================

    @commands.command(name="getheaders", aliases=["headers"])
    async def _getheaders(
        self, ctx: commands.Context, ip: str, *, user_agent: str = ""
    ):
        if not ip.startswith("http"):
            ip = f"http://{ip}"

        await self.__check_for_rfc1918_or_raise(ip)

        session, headers = await self.__get_headers(ip, user_agent)
        colors = {
            "1": 0x17A2B8,
            "2": 0x28A745,
            "3": 0xFFC107,
            "4": 0xDC3545,
            "5": 0x343A40,
        }

        e = discord.Embed(
            title=f"Headers : {ip}",
            color=colors.get(str(session.status)[0], 0x6C757D),
        )
        e.add_field(
            name="Status", value=f"```{session.status}```", inline=True
        )
        e.set_thumbnail(url=f"https://http.cat/{session.status}")

        for key, value in headers.items():
            _, output = await self.bot.utils.shorten(value, 50)

            if output["link"]:
                value = f"[show all]({output['link']})"
            else:
                value = f"```\n{output['text']}```"

            e.add_field(name=key, value=value, inline=True)

        await ctx.send(embed=e)
