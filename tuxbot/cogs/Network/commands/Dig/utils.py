"""
tuxbot.cogs.Network.functions.Dig.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""

import asyncio
from typing import Any, Dict

import aiohttp
from bs4 import BeautifulSoup


def parse_from_bortzmeyer(html: str) -> Dict[str, Any]:
    """Parse HTML result as dict object"""

    soup = BeautifulSoup(html, "html.parser")

    body = soup.find(class_="body")

    try:
        return {
            "header": soup.find(name="h1").text,
            "body": list(map(lambda el: el.text, body.select("li>span"))),
            "footer": body.find(name="p").text,
        }
    except AttributeError:
        return {}


async def get_from_bortzmeyer(domain: str, query_type: str) -> Dict[str, Any]:
    """Get result from https://dns.bortzmeyer.org/"""

    try:
        async with aiohttp.ClientSession() as cs, cs.get(
            f"https://dns.bortzmeyer.org/{domain}/{query_type}",
            timeout=aiohttp.ClientTimeout(total=2),
        ) as s:
            return parse_from_bortzmeyer(await s.text())
    except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
        pass

    return {}
