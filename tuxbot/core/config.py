import logging
from typing import List, Dict, Any, NoReturn
from structured_config import (
    Structure,
    IntField,
    StrField,
    BoolField,
    ConfigFile,
)


__all__ = [
    "Config",
    "ConfigFile",
    "AppConfig",
    "search_for",
    "set_for_key",
    "set_for",
]

log = logging.getLogger("tuxbot.core.config")


class Config(Structure):
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

    class Cog(Structure):
        pass

    Servers: Dict[int, Server] = {}
    Channels: Dict[int, Channel] = {}
    Users: Dict[int, User] = {}
    Cogs: Dict[str, Cog] = {}

    class Core(Structure):
        owners_id: List[int] = []
        prefixes: List[str] = []
        token: str = StrField("")
        mentionable: bool = BoolField("")
        locale: str = StrField("")
        disabled_command: List[str] = []


# =============================================================================
# Configuration of Tuxbot Application (not the bot)
# =============================================================================


class AppConfig(Structure):
    class Instance(Structure):
        path: str = StrField("")
        active: bool = BoolField(False)
        last_run: int = IntField(0)

    Instances: Dict[str, Instance] = {}


# =============================================================================
# Useful functions to interact with configs
# =============================================================================


def search_for(config, key, value, default=False) -> Any:
    if key in config:
        return getattr(config[key], value)
    return default


def set_for_key(config, key, ctype, **values) -> NoReturn:
    # pylint: disable=anomalous-backslash-in-string
    """
    La fonction suivante        \`*-.
    a été écrite le lundi        )  _`-.
    19 octobre 2020 a 13h40     .  : `. .
    soit 1h apres la découverte : _   '  \
    du corps de mon chat        ; *` _.   `*-._
                                `-.-'          `-.
                                  ;       `       `.
                                  :.       .        \
                                  . \  .   :   .-'   .
                                  '  `+.;  ;  '      :
                                  :  '  |    ;       ;-.
                                  ; '   : :`-:     _.`* ;
               rip roxy        .*' /  .*' ; .*`- +'  `*'
           201?-2020 :,(       `*-*   `*-*  `*-*'
    """
    if key not in config:
        config[key] = ctype()

    for k, v in values.items():
        setattr(config[key], k, v)


def set_for(config, **values) -> NoReturn:
    for k, v in values.items():
        setattr(config, k, v)
