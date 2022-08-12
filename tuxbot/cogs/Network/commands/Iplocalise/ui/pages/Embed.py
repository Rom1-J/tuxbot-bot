"""
Base embed page
"""
import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class Embed:
    """Base embed page"""

    def __init__(self, controller: "ViewController") -> None:
        self.controller = controller
        self.data = self.controller.data

        self.ctx = self.controller.ctx

    # =========================================================================
    # =========================================================================

    def update(self, controller: "ViewController") -> None:
        """Update loaded data"""
        self.controller = controller
        self.data = self.controller.data

    # =========================================================================

    def rebuild(self) -> discord.Embed:
        """(Re)build embed"""
