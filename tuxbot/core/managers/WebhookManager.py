"""
Tuxbot manager module: WebhookManager

Contains all webhooks management
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class WebhookManager:
    """Tuxbot webhook manager"""
    def __init__(self, tuxbot: "Tuxbot"):
        self.tuxbot = tuxbot
