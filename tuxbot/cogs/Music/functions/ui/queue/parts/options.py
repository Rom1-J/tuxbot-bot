from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Track


class TrackOption(discord.SelectOption):
    track: Optional[Track]

    def __init__(self, **kwargs):
        self.track: Track = kwargs.pop("track", None)

        super().__init__(**kwargs)
