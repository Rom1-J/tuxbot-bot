from abc import ABC
from typing import Optional


class Provider(ABC):
    def __init__(self, apikey: Optional[str] = None):
        self.apikey = apikey

    # pylint: disable=unused-argument
    async def fetch(self, ip: str) -> dict:
        ...
