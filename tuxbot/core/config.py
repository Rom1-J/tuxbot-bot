import asyncio
import logging
from typing import List, Dict
from structured_config import (
    ConfigFile,
    Structure, IntField, StrField, BoolField
)

import discord

from tuxbot.core.data_manager import data_path

__all__ = ["Config"]

log = logging.getLogger("tuxbot.core.config")


class Server(Structure):
    prefixes: List[str] = []
    disabled_command: List[str] = []
    locale: str = StrField("")


class User(Structure):
    aliases: List[dict] = []
    locale: str = StrField("")


class Config(Structure):
    class Servers(Structure):
        count: int = IntField(0)
        all: List[Server] = []

    class Users(Structure):
        all: List[User] = []

    class Core(Structure):
        owners_id: List[int] = []
        prefixes: List[str] = []
        token: str = StrField("")
        mentionable: bool = BoolField("")
        locale: str = StrField("")

    class Cogs(Structure):
        pass


# =============================================================================
# Configuration of Tuxbot Application (not the bot)
# =============================================================================

class Instance(Structure):
    path: str = StrField("")
    active: bool = BoolField(False)


class AppConfig(Structure):
    instances: Dict[str, Instance] = {}
