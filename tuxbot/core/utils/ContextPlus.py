"""
Custom Context class
"""
from typing import TYPE_CHECKING, Any, Sequence

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

        return "<{} {}>".format(self.__class__.__name__, ", ".join(items))

    # =========================================================================

    def _clean_message(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        def clear_embeds(_embeds: list[Embed]):
            """Clear embed from sensitive data"""

            es = _embeds.copy()

            for i, e in enumerate(es):
                e = e.to_dict()

                for key, value in e.items():
                    if isinstance(value, str):
                        # noinspection PyTypedDict
                        e[key] = value.replace(
                            self.bot.http.token, "[redacted]"
                        )

                es[i] = Embed.from_dict(e)

            return es

        if content := kwargs.get("content"):
            kwargs["content"] = content.replace(
                self.bot.http.token, "[redacted]"
            )

        if embed := kwargs.get("embed"):
            kwargs["embed"] = clear_embeds([embed])[0]

        if embeds := kwargs.get("embeds"):
            kwargs["embeds"] = clear_embeds(embeds)

        return kwargs

    # =========================================================================

    # pylint: disable=too-many-locals
    async def send(
        self,
        content: str | None = None,
        *,
        tts: bool = False,
        embed: Embed | None = None,
        embeds: Sequence[Embed] | None = None,
        file: File | None = None,
        files: Sequence[File] | None = None,
        stickers: Sequence[GuildSticker | StickerItem] | None = None,
        delete_after: float | None = None,
        nonce: str | int | None = None,
        allowed_mentions: AllowedMentions | None = None,
        reference: None | (Message | MessageReference | PartialMessage) = None,
        mention_author: bool | None = None,
        view: View | None = None,
        suppress_embeds: bool = False,
        ephemeral: bool = False,
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
            "reference": reference or self.message,
            "mention_author": mention_author or False,
            "view": view,
            "suppress_embeds": suppress_embeds,
            "ephemeral": ephemeral,
        }

        kwargs = self._clean_message(kwargs)

        # noinspection PyArgumentList
        return await super().send(**kwargs)
