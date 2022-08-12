"""
tuxbot.cogs.Linux.commands.CNF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command-not-found scrapper and parser
"""
import asyncio
import typing

import aiohttp
import bs4
from bs4 import BeautifulSoup

from .exceptions import CNFException


class CNF:
    """command-not-found scrapper"""

    _url = "https://command-not-found.com/{}"
    _content: BeautifulSoup | None = None

    command: str

    description: str = ""
    meta: dict[str, typing.Any] | None = None
    distro: dict[str, typing.Any] | None = None

    def __init__(self, command: str):
        self.command = command

        self.description = ""
        self.meta = {}
        self.distro = {}

    # =========================================================================
    # =========================================================================

    async def fetch(self) -> None:
        """Fetch from https://command-not-found.com/"""

        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                self._url.format(self.command)
            ) as s:
                if s.status == 200:
                    self._content = BeautifulSoup(
                        await s.text(), "html.parser"
                    )
                    self.parse()
                    return

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise CNFException("Something went wrong ...")

    # =========================================================================

    def parse(self) -> None:
        """Parse page content to extract needed packages"""
        if not self._content:
            raise ValueError

        info = self._content.find("div", class_="row-command-info")
        distro = self._content.find_all("div", class_="command-install")

        self.description = "N/A"
        self.meta = {}
        self.distro = {}

        if isinstance(info, bs4.Tag):
            if res := info.find("p", class_="my-0"):
                self.description = res.text.strip()

            if (res := info.find("ul", class_="list-group")) and isinstance(
                res, bs4.Tag
            ):
                for m in res.find_all("li"):
                    row = m.text.strip().split("\n")

                    self.meta[row[0].lower()[:-1]] = row[1]

        if len(distro) > 1:
            del distro[0]  # unused row

            for d in distro:
                self.distro[
                    d.find("dt").text.strip().split("\n")[-1].strip()
                ] = d.find("code").text

    # =========================================================================

    def to_dict(self) -> dict[str, typing.Any]:
        """Return result as dict

        Returns
        -------
        dict[str, typing.Any]
        """

        return {
            "command": self.command,
            "description": self.description,
            "meta": self.meta,
            "distro": self.distro,
        }


async def get_from_cnf(command: str) -> dict[str, typing.Any]:
    """Simple function to use CNF class

    Parameters
    ----------
    command: str
        Command to search for

    Returns
    -------
    dict[str, typing.Any]
    """
    cnf = CNF(command)
    await cnf.fetch()

    return cnf.to_dict()
