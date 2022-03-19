"""
Custom Context class
"""
from typing import TYPE_CHECKING, List, Optional, Sequence, Union

from discord import (
    AllowedMentions,
    Embed,
    File,
    GuildSticker,
    Message,
    MessageReference,
    PartialMessage,
    StickerItem,
)
from discord.ext import commands
from discord.ui import View

if TYPE_CHECKING:
    from tuxbot.abc.TuxbotABC import TuxbotABC


class ContextPlus(commands.Context):
    """Extended Context class with new/rewrote features"""

    bot: "TuxbotABC"

    def __repr__(self):
        items = (
            "message=%s" % self.message,
            "channel=%s" % self.channel,
            "guild=%s" % self.guild,
            "author=%s" % self.author,
            "prefix=%s" % self.prefix,
            "args=%s" % self.args,
            "kwargs=%s" % self.kwargs,
        )

        return "<%s %s>" % (self.__class__.__name__, ", ".join(items))

    # =========================================================================

    def _clean_message(self):
        ...

    # =========================================================================

    # pylint: disable=too-many-locals
    async def send(
        self,
        content: Optional[str] = None,
        *,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        file: Optional[File] = None,
        files: Optional[List[File]] = None,
        stickers: Optional[Sequence[Union[GuildSticker, StickerItem]]] = None,
        delete_after: Optional[float] = None,
        nonce: Optional[Union[str, int]] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        reference: Optional[
            Union[Message, MessageReference, PartialMessage]
        ] = None,
        mention_author: Optional[bool] = None,
        view: Optional[View] = None,
        suppress_embeds: bool = False,
    ) -> Message:
        """Proxy function for internal ctx.`send` of dpy"""

        kwargs = {
            "content": content,
            "tts": tts,
            "embed": embed,
            "embeds": embeds,
            "file": file,
            "files": files,
            "stickers": stickers,
            "delete_after": delete_after,
            "nonce": nonce,
            "allowed_mentions": allowed_mentions,
            "reference": reference,
            "mention_author": mention_author,
            "view": view,
            "suppress_embeds": suppress_embeds,
        }

        self.bot.logger.debug(kwargs)

        # noinspection PyArgumentList
        return await super().send(**kwargs)
