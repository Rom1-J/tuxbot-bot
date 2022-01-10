"""
Tuxbot commands module: Admin

Set of all admin only commands
"""
from typing import Any

from tuxbot.abc.ModuleABC import ModuleABC

from tuxbot.core.Tuxbot import Tuxbot


class AdminModule(ModuleABC):
    """Tuxbot owner only commands"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self.name = "Admin"
        self.description = "Tuxbot owner only commands"

        self.enabled = True

        super(ModuleABC, self).__init__()

    # =========================================================================

    def register_listener(self, event: str, *args: Any, **kwargs: Any):
        """Register listener"""
        pass

    def crash_report(self):
        """Crash report handler"""
        pass

