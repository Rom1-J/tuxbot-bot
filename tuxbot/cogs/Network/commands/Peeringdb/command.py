"""
tuxbot.cogs.Network.commands.Peeringdb.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows information from peeringdb about an ASN
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, NoReturn, Union

import aiohttp
import discord
from aiohttp import TCPConnector
from discord.ext import commands, tasks  # type: ignore

from tuxbot.core.Tuxbot import Tuxbot

from .converters.ASConverter import ASConverter
from .exceptions import InvalidAsn


class PeeringdbCommand(commands.Cog):
    """Shows information about given ASN"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self._peeringdb_net = None
        self._update_peering_db.start()  # pylint: disable=no-member

    # =========================================================================

    async def cog_unload(self):
        """Stop task updater"""
        self.bot.logger.info("[PeeringdbCommand Canceling _update_peering_db")
        self._update_peering_db.cancel()  # pylint: disable=no-member

    # =========================================================================
    # =========================================================================

    @staticmethod
    def __check_asn_or_raise(asn: str) -> Union[bool, NoReturn]:
        """Validate asn format"""

        if asn.isdigit() and int(asn) < 4_294_967_295:
            return True

        raise InvalidAsn("Invalid ASN provided")

    # =========================================================================
    # =========================================================================

    @tasks.loop(hours=6.00)
    async def _update_peering_db(self):
        try:
            async with aiohttp.ClientSession(
                connector=TCPConnector(verify_ssl=False)
            ) as cs, cs.get(
                "https://peeringdb.com/api/net",
                timeout=aiohttp.ClientTimeout(total=60),
            ) as s:
                self._peeringdb_net = await s.json()
        except asyncio.exceptions.TimeoutError:
            pass
        else:
            self.bot.logger.info("[PeeringdbCommand] _update_peering_db done!")

    # =========================================================================
    # =========================================================================

    @commands.command(name="peeringdb", aliases=["peer", "peering"])
    async def _peeringdb(self, ctx: commands.Context, asn: ASConverter):
        if (
            # pylint: disable=no-member
            not self._update_peering_db.is_running()
        ):
            self._peeringdb_net = None
            self._update_peering_db.start()  # pylint: disable=no-member

        self.__check_asn_or_raise(str(asn))

        data: Dict[str, Any] = {}

        if self._peeringdb_net is None:
            return await ctx.send("Please retry in few seconds.")

        for _data in self._peeringdb_net["data"]:
            if _data.get("asn", None) == int(str(asn)):
                data = _data
                break

        if not data:
            return await ctx.send(
                f"AS{asn} could not be found in PeeringDB's database."
            )

        filtered = {
            "info_type": "Type",
            "info_traffic": "Traffic",
            "info_ratio": "Ratio",
            "info_prefixes4": "Prefixes IPv4",
            "info_prefixes6": "Prefixes IPv6",
        }
        filtered_link = {
            "website": ("Site", "website"),
            "looking_glass": ("Looking Glass", "looking_glass"),
            "policy_general": ("Peering", "policy_url"),
        }

        e = discord.Embed(
            title=f"{data['name']} ({data.get('aka') or f'AS{asn}'})",
            color=0x5858D7,
        )

        for key, name in filtered.items():
            e.add_field(name=name, value=f"```{data.get(key) or 'N/A'}```")

        for key, names in filtered_link.items():
            if data.get(key):
                e.add_field(
                    name=names[0],
                    value=f"[{data.get(key) or 'N/A'}]"
                    f"({data.get(names[1]) or 'N/A'})",
                )

        if data["notes"]:
            output = (await self.bot.utils.shorten(data["notes"], 550))[1]
            e.description = output["text"]
        if data["created"]:
            e.timestamp = datetime.strptime(
                data["created"], "%Y-%m-%dT%H:%M:%SZ"
            )

        await ctx.send(f"https://www.peeringdb.com/net/{data['id']}", embed=e)
