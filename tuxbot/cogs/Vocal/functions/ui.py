import datetime
from os.path import dirname
from typing import Optional

import discord
from tuxbot.core.i18n import Translator
from .utils import Player, Track


_ = Translator("Vocal", dirname(__file__))


class PlaylistSelect(discord.ui.Select):
    def __init__(
        self, options: list, author: discord.User, page=0, ephemeral=False
    ):
        self._page = page
        self._options = options

        self._author = author
        self._ephemeral = ephemeral

        super().__init__(
            placeholder=f"Page: {self._page + 1}/{len(self._options)}",
            min_values=1,
            max_values=1,
            options=self._options[self._page],
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.data["values"][0] == "more":
            return await self._update_page(interaction, +1)

        if interaction.data["values"][0] == "less":
            return await self._update_page(interaction, -1)

        await interaction.response.send_message(
            content="Not implemented yet", ephemeral=True
        )

    def _check_author(self, interaction: discord.Interaction):
        return interaction.user == self._author

    async def _update_page(self, interaction: discord.Interaction, page: int):
        view = discord.ui.View()

        if self._check_author(interaction):
            self._page += page
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

            view.add_item(self)
            await interaction.response.edit_message(
                content="Music on hold:", view=view
            )
        else:
            select = PlaylistSelect(
                self._options,
                interaction.user,
                page=self._page + page,
                ephemeral=True,
            )
            view.add_item(select)

            await interaction.response.send_message(
                content="Music on hold:", view=view, ephemeral=True
            )


class ControllerView(discord.ui.View):
    def __init__(self, *args, author: discord.User, player: Player, **kwargs):
        super().__init__(*args, **kwargs)

        self._author = author
        self._player = player

        print(self.children)

    # =========================================================================
    # =========================================================================

    @discord.ui.button(
        emoji="<:trash_w:863163000038227998>",
        row=0,
        style=discord.ButtonStyle.danger,
    )
    async def _remove(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        return

    @discord.ui.button(
        emoji="<:vol_up_w:863163026470076447>",
        row=0,
        style=discord.ButtonStyle.primary,
    )
    async def _vol_up(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("vol up...", ephemeral=True)

    @discord.ui.button(emoji="<:shuffle_w:863162986184310828>", row=0)
    async def _shuffle(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("shuffle...", ephemeral=True)

    # =========================================================================

    @discord.ui.button(
        emoji="<:prev_song_w:863162971802042400>",
        row=1,
        style=discord.ButtonStyle.primary,
    )
    async def _prev(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("previous...", ephemeral=True)

    @discord.ui.button(
        emoji="<:play_song_w:863162951032766494>",
        row=1,
        style=discord.ButtonStyle.primary,
    )
    async def _toggle(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        button.emoji = (
            "<:play_song_w:863162951032766494>"
            if str(button.emoji) == "<:pause_song_w:863162917595906048>"
            else "<:pause_song_w:863162917595906048>"
        )
        await interaction.response.edit_message(view=self)

    @discord.ui.button(
        emoji="<:next_song_w:863162901820735538>",
        row=1,
        style=discord.ButtonStyle.primary,
    )
    async def _next(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("next...", ephemeral=True)

    # =========================================================================

    @discord.ui.button(
        disabled=True, emoji="<:blank:863085374640488518>", row=2
    )
    async def _blank3(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        return

    @discord.ui.button(
        emoji="<:vol_down_w:863163012927848484>",
        row=2,
        style=discord.ButtonStyle.primary,
    )
    async def _vol_down(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("vol down...", ephemeral=True)

    @discord.ui.button(emoji="<:playlist_w:863162933211037726>", row=2)
    async def _queue(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("queue...", ephemeral=True)

    # =========================================================================
    # =========================================================================

    def build_embed(self) -> Optional[discord.Embed]:
        track: Track = self._player.current
        if not track:
            return None

        qsize = self._player.queue.qsize()

        e = discord.Embed(colour=0x2F3136)
        e.add_field(
            name=f"{track.emoji} {track.author}",
            value=(
                f"[{track.title}]"
                f"({track.uri})"
            ),
            inline=False,
        )
        if track.thumb:
            e.set_image(url=track.thumb)

        e.add_field(
            name=_(
                "Duration",
                self._player.context,
                self._player.context.bot.config
            ),
            value=str(datetime.timedelta(milliseconds=int(track.length))),
            inline=True,
        )
        e.add_field(
            name="Volume",
            value=f"**`{self._player.volume}%`**",
            inline=True
        )
        e.add_field(
            name="DJ",
            value=self._player.dj.mention,
            inline=True
        )

        e.set_footer(
            text=_(
                "Requested by {name} | Position in queue: {pos}/{total}",
                self._player.context,
                self._player.context.bot.config
            ).format(name=str(track.requester), pos=str(-1), total=str(qsize))
        )

        return e
