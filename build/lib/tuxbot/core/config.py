from pathlib import Path
from typing import Any, NoReturn


class Config:
    GLOBAL = "GLOBAL"
    GUILD = "GUILD"
    CHANNEL = "TEXT_CHANNEL"
    ROLE = "ROLE"
    MEMBER = "MEMBER"
    USER = "USER"

    def __init__(self, config_dir: Path):
        self._defaults = {}

    def __getattr__(self, item: str) -> dict:
        return getattr(self._defaults, item)

    def _register_default(self, key: str, **kwargs: Any):
        ...

    def register_core(self, **kwargs) -> NoReturn:
        self._register_default(self.GUILD, **kwargs)

    def register_global(self, **kwargs) -> NoReturn:
        self._register_default(self.GLOBAL, **kwargs)

    def register_guild(self, **kwargs) -> NoReturn:
        self._register_default(self.GUILD, **kwargs)

    def register_channel(self, **kwargs) -> NoReturn:
        self._register_default(self.CHANNEL, **kwargs)

    def register_role(self, **kwargs) -> NoReturn:
        self._register_default(self.ROLE, **kwargs)

    def register_member(self, **kwargs) -> NoReturn:
        self._register_default(self.MEMBER, **kwargs)

    def register_user(self, **kwargs) -> NoReturn:
        self._register_default(self.USER, **kwargs)
