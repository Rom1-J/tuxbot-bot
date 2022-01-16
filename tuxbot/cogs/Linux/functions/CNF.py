"""
tuxbot.cogs.Linux.functions.CNF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command-not-found scrapper and parser
"""

import asyncio
from typing import Dict, Union

import aiohttp
from bs4 import BeautifulSoup

from .exceptions import CNFException


class CNF:
    """command-not-found scrapper"""

    _url = "https://command-not-found.com/{}"
    _content: BeautifulSoup = None

    command: str

    description: str = ""
    meta: dict = None
    distro: dict = None

    def __init__(self, command: str):
        self.command = command

        self.description = ""
        self.meta = {}
        self.distro = {}

    # =========================================================================
    # =========================================================================

    async def fetch(self):
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

    def parse(self):
        """Parse page content to extract needed packages"""

        info = self._content.find("div", class_="row-command-info")
        distro = self._content.find_all("div", class_="command-install")

        try:
            self.description = info.find("p", class_="my-0").text.strip()
        except AttributeError:
            self.description = "N/A"

        try:
            for m in info.find("ul", class_="list-group").find_all("li"):
                row = m.text.strip().split("\n")

                self.meta[row[0].lower()[:-1]] = row[1]
        except AttributeError:
            self.meta = {}

        try:
            del distro[0]  # unused row

            for d in distro:
                self.distro[
                    d.find("dt").text.strip().split("\n")[-1].strip()
                ] = d.find("code").text
        except (AttributeError, IndexError):
            self.distro = {}

    # =========================================================================

    def to_dict(self) -> Dict[str, Union[str, dict]]:
        """Return result as dict

        Returns
        -------
        Dict[str, str]
        """

        return {
            "command": self.command,
            "description": self.description,
            "meta": self.meta,
            "distro": self.distro,
        }


async def get_from_cnf(command: str) -> Dict[str, Union[str, dict]]:
    """Simple function to use CNF class

    Parameters
    ----------
    command: str
        Command to search for

    Returns
    -------
    Dict[str, Union[str, dict]]
    """
    cnf = CNF(command)
    await cnf.fetch()

    return cnf.to_dict()
