import logging
from typing import List, Dict, Any
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
    "search_for",
    "set_for_key",
    "set_for",
    "set_if_none",
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
        aliases: dict = {}
        locale: str = StrField("")
        blacklisted: bool = BoolField(False)

    class Cog(Structure):
        pass

    Servers: Dict[int, Server] = {}
    Channels: Dict[int, Channel] = {}
    Users: Dict[int, User] = {}
    Cogs: Dict[str, Cog] = {}

    class Core(Structure):
        class Database(Structure):
            username: str = StrField("")
            password: str = StrField("")
            domain: str = StrField("")
            port: str = IntField(5432)
            db_name: str = StrField("")

        owners_id: List[int] = []
        prefixes: List[str] = []
        token: str = StrField("")
        ip: str = StrField("")
        ip6: str = StrField("")
        mentionable: bool = BoolField("")
        locale: str = StrField("")
        disabled_command: List[str] = []
        instance_name: str = StrField("")


# =============================================================================
# Useful functions to interact with configs
# =============================================================================


def search_for(config, key, value, default=False) -> Any:
    if key in config:
        return getattr(config[key], value)
    return default


def set_if_none(config, key, ctype) -> None:
    if key not in config:
        config[key] = ctype()


def set_for_key(config, key, ctype, **values) -> None:
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
    set_if_none(config, key, ctype)

    for k, v in values.items():
        setattr(config[key], k, v)


def set_for(config, **values) -> None:
    for k, v in values.items():
        setattr(config, k, v)
