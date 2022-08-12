"""
Base embed page
"""
import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class Embed:
    """Base embed page"""

    def __init__(self, controller: "ViewController"):
        self.controller = controller
        self.model = self.controller.model

        self.ctx = self.controller.ctx

    # =========================================================================
    # =========================================================================

    def rebuild(self) -> discord.Embed:
        """(Re)build embed"""
