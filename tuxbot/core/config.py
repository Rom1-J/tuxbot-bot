import logging
from typing import List, Dict
from structured_config import (
    Structure,
    IntField,
    StrField,
    BoolField,
    ConfigFile,
)


__all__ = ["Config", "ConfigFile"]

log = logging.getLogger("tuxbot.core.config")


class Server(Structure):
    prefixes: List[str] = []
    disabled_command: List[str] = []
    locale: str = StrField("")
    blacklisted: bool = BoolField(False)


class Channel(Structure):
    disabled_command: List[str] = []
    locale: str = StrField("")
    blacklisted: bool = BoolField(False)


class User(Structure):
    aliases: List[dict] = []
    locale: str = StrField("")
    blacklisted: bool = BoolField(False)


class Config(Structure):
    class Servers(Structure):
        all: Dict[int, Server] = {}

    class Channels(Structure):
        all: Dict[int, Channel] = {}

    class Users(Structure):
        all: Dict[int, User] = {}

    class Core(Structure):
        owners_id: List[int] = []
        prefixes: List[str] = []
        token: str = StrField("")
        mentionable: bool = BoolField("")
        locale: str = StrField("")
        disabled_command: List[str] = []

    class Cogs(Structure):
        pass


# =============================================================================
# Configuration of Tuxbot Application (not the bot)
# =============================================================================


class AppConfig(Structure):
    class Instance(Structure):
        path: str = StrField("")
        active: bool = BoolField(False)
        last_run: int = IntField(0)

    instances: Dict[str, Instance] = {}
