from abc import ABC
from typing import Optional


class Provider(ABC):
    def __init__(self, apikey: Optional[str] = None):
        self.apikey = apikey

    async def fetch(self, ip: str) -> dict:
        raise NotImplementedError
