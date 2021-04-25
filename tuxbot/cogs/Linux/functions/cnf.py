import asyncio

import aiohttp
from bs4 import BeautifulSoup

from tuxbot.cogs.Linux.functions.exceptions import CNFException


def _(x):
    return x


class CNF:
    _url = "https://command-not-found.com/{}"
    _content: BeautifulSoup

    command: str

    description: str = ""
    meta: dict = {}
    distro: dict = {}

    def __init__(self, command: str):
        self.command = command

    # =========================================================================
    # =========================================================================

    async def fetch(self):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(self._url.format(self.command)) as s:
                    if s.status == 200:
                        self._content = BeautifulSoup(
                            await s.text(), "html.parser"
                        )
                        return self.parse()

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise CNFException(_("Something went wrong ..."))

    def parse(self):
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

    def to_dict(self):
        return {
            "command": self.command,
            "description": self.description,
            "meta": self.meta,
            "distro": self.distro,
        }
