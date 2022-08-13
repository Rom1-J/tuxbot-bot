"""
Custom Context class
"""
import typing

import discord
from discord.ext import commands
from discord.ui import View


if typing.TYPE_CHECKING:
    from tuxbot.abc.TuxbotABC import TuxbotABC


class ContextPlus(commands.Context["TuxbotABC"]):
    """Extended Context class with new/rewrote features"""

    bot: "TuxbotABC"

    def __repr__(self) -> str:
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

    def _clean_message(
        self, kwargs: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        if not self.bot.http.token:
            return kwargs

        def clear_embeds(_embeds: list[discord.Embed]) -> list[discord.Embed]:
            """Clear embed from sensitive data"""
            if not self.bot.http.token:
                return _embeds

            es = _embeds.copy()

            for i, e in enumerate(es):
                e_dict = e.to_dict()

                for key, value in e_dict.items():
                    if isinstance(value, str):
                        # noinspection PyTypedDict
                        e_dict[key] = value.replace(  # type: ignore
                            self.bot.http.token, "[redacted]"
                        )

                es[i] = discord.Embed.from_dict(e_dict)

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
        embed: discord.Embed | None = None,
        embeds: typing.Sequence[discord.Embed] | None = None,
        file: discord.File | None = None,
        files: typing.Sequence[discord.File] | None = None,
        stickers: typing.Sequence[discord.GuildSticker | discord.StickerItem]
        | None = None,
        delete_after: float | None = None,
        nonce: str | int | None = None,
        allowed_mentions: discord.AllowedMentions | None = None,
        reference: None
        | (
            discord.Message | discord.MessageReference | discord.PartialMessage
        ) = None,
        mention_author: bool | None = None,
        view: View | None = None,
        suppress_embeds: bool = False,
        ephemeral: bool = False,
    ) -> discord.Message:
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

        return await super().send(**kwargs)  # type: ignore
