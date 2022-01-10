"""
Tuxbot manager module: PermissionsManager

Contains all permissions management
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class PermissionsManager:
    """Tuxbot permissions manager"""
    def __init__(self, tuxbot: "Tuxbot"):
        self.tuxbot = tuxbot
