import logging

import math
from os.path import dirname

from typing import Optional, List, Set

import discord
import wavelink

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus
from tuxbot.core.i18n import Translator
from .exceptions import TrackTooLong
from .ui.controller.view import ControllerView
from .ui.queue.view import QueueView

log = logging.getLogger("tuxbot.cogs.Music")
_ = Translator("Music", dirname(__file__))


class Track(wavelink.Track):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")
        self.emoji = self.get_emoji(kwargs.get("query", ""))

    @staticmethod
    def get_emoji(query: str) -> str:
        transform = {
            "youtube": "<:youtube:862463749273026561>",
            "ytsearch": "<:youtube:862463749273026561>",
            "spotify": "<:spotify:862463903959351309>",
            "soundcloud": "<:soundcloud:862464041121087518>",
            "vimeo": "<:vimeo:863181307424407552>",
            "bandcamp": "<:bandcamp:863182155084464138>",
        }

        for key, value in transform.items():
            if key in query.replace(".", ""):
                return value

        return "🎵"

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Track requester="%s" title="%s">' % (
            str(self.requester),
            self.title,
        )


class Player(wavelink.Player):
    bot: Tux
    controller: Optional[discord.Message]
    controller_view: Optional[ControllerView]

    last_played_position: int = -1
    track_position: int = -1

    def __init__(self, bot: Tux, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)

        self.context: ContextPlus = kwargs.get("context")
        if self.context:
            self.dj: discord.Member = self.context.author

        self.queue: List[Track] = []

        self.controller: Optional[discord.Message] = None
        self.controller_view: Optional[discord.Message] = None

        self.waiting = False
        self.updating = False

        self.pause_votes: Set[discord.Member] = set()
        self.resume_votes: Set[discord.Member] = set()
        self.back_votes: Set[discord.Member] = set()
        self.skip_votes: Set[discord.Member] = set()
        self.shuffle_votes: Set[discord.Member] = set()
        self.end_votes: Set[discord.Member] = set()
        self.delete_votes: Set[discord.Member] = set()

    async def toggle_pause(self, user: discord.Member):
        if self.is_paused:
            action = (
                _("resume", self.context, self.bot.config),
                _("resumed", self.context, self.bot.config),
                _("Resuming", self.context, self.bot.config),
            )
        else:
            action = (
                _("pause", self.context, self.bot.config),
                _("paused", self.context, self.bot.config),
                _("Pausing", self.context, self.bot.config),
            )

        if self.is_privileged(user):
            await self.context.send(
                _(
                    "An admin or DJ has {action} the song.",
                    self.context,
                    self.bot.config,
                ).format(action=action[1]),
                delete_after=15,
            )

            self.pause_votes.clear()
            await self.set_pause(not self.is_paused)

            return await self.invoke_controller()

        required = self.required()
        self.pause_votes.add(user)

        if len(self.pause_votes) >= required:
            await self.context.send(
                _(
                    "Vote to {actionA} passed. {actionB} the song.",
                    self.context,
                    self.bot.config,
                ).format(actionA=action[0], actionB=action[2]),
                delete_after=15,
            )

            self.pause_votes.clear()
            await self.set_pause(not self.is_paused)

            return await self.invoke_controller()

        await self.context.send(
            _(
                "{name} has voted to {action} this song.",
                self.context,
                self.bot.config,
            ).format(name=user.mention, action=action[0]),
            delete_after=15,
        )

    async def back(self, user: discord.Member):
        if self.is_privileged(user):
            await self.context.send(
                _(
                    "An admin or DJ has go back on the previous song",
                    self.context,
                    self.bot.config,
                ),
                delete_after=15,
            )

            self.back_votes.clear()
            return await self.back_queue()

        required = self.required()
        self.back_votes.add(user)

        if len(self.back_votes) >= required:
            await self.context.send(
                _(
                    "Vote to go back passed. Going back on the previous song.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=15,
            )

            self.back_votes.clear()
            return await self.back_queue()

        await self.context.send(
            _(
                "{name} has voted to go back on the previous song.",
                self.context,
                self.bot.config,
            ).format(name=user.mention),
            delete_after=15,
        )

    async def skip(self, user: discord.Member):
        if self.is_privileged(user):
            await self.context.send(
                _(
                    "An admin or DJ has skipped the song.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=15,
            )

            self.skip_votes.clear()
            return await self.skip_queue()

        required = self.required()
        self.back_votes.add(user)

        if len(self.back_votes) >= required:
            await self.context.send(
                _(
                    "Vote to skip passed. Skipping the song.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=15,
            )

            self.skip_votes.clear()
            return await self.skip_queue()

        await self.context.send(
            _(
                "{name} has voted to skip the song.",
                self.context,
                self.bot.config,
            ).format(name=user.mention),
            delete_after=15,
        )

    async def jump(self, user: discord.Member, track: Track):
        if self.is_privileged(user):
            await self.context.send(
                _(
                    "An admin or DJ went directly to the song __{track}__.",
                    self.context,
                    self.bot.config,
                ).format(track=str(track)),
                delete_after=15,
            )

            self.skip_votes.clear()
            return await self.jump_queue(track)

        required = self.required()
        self.back_votes.add(user)

        if len(self.back_votes) >= required:
            await self.context.send(
                _(
                    "Vote to go to __{track}__. Jumping to the song.",
                    self.context,
                    self.bot.config,
                ).format(track=str(track)),
                delete_after=15,
            )

            self.skip_votes.clear()
            return await self.jump_queue(track)

        await self.context.send(
            _(
                "{name} has voted to go to the song __{track}__.",
                self.context,
                self.bot.config,
            ).format(name=user.mention, track=str(track)),
            delete_after=15,
        )

    # pylint: disable=unused-argument
    async def shuffle(self, user: discord.Member):
        await self.context.send(
            "shuffle not implemented yet...", delete_after=5
        )

    async def end(self, user: discord.Member):
        if self.is_privileged(user):
            self.end_votes.clear()

            if self.controller:
                await self.controller.delete()
            else:
                await self.terminate()
                return await self.context.send(
                    _(
                        "There was no controller to stop.",
                        self.context,
                        self.bot.config,
                    ),
                    delete_after=15,
                )

            await self.terminate()
            return await self.context.send(
                _(
                    "Disconnected player and killed controller.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=15,
            )

        required = self.required(stop=True)
        self.end_votes.add(user)

        if len(self.end_votes) >= required:
            await self.context.send(
                _(
                    "Vote to end passed. Ending session.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=15,
            )
            self.end_votes.clear()
            return await self.terminate()

        await self.context.send(
            _(
                "{name} has voted to end this session.",
                self.context,
                self.bot.config,
            ).format(name=user.mention),
            delete_after=15,
        )

    async def delete(self, user: discord.Member, track: Track):
        if self.is_privileged(user):
            await self.context.send(
                _(
                    "An admin or DJ has removed the song __{track}__.",
                    self.context,
                    self.bot.config,
                ).format(track=str(track)),
                delete_after=15,
            )

            self.delete_votes.clear()
            return await self.remove_queue(track)

        required = self.required()
        self.delete_votes.add(user)

        if len(self.delete_votes) >= required:
            await self.context.send(
                _(
                    "Vote to remove __{track}__ passed. Removing the song.",
                    self.context,
                    self.bot.config,
                ).format(track=str(track)),
                delete_after=15,
            )

            self.delete_votes.clear()
            return await self.remove_queue(track)

        await self.context.send(
            _(
                "{name} has voted to remove the song __{track}__.",
                self.context,
                self.bot.config,
            ).format(name=user.mention, track=str(track)),
            delete_after=15,
        )

    async def playlist(
        self,
        user: discord.Member,
        interaction: Optional[discord.Interaction] = None,
    ):
        view = QueueView(author=user, player=self)

        if interaction:
            await interaction.response.send_message(
                "Music on hold:", view=view, ephemeral=True
            )
        else:
            await self.context.send("Music on hold:", view=view)

    # =========================================================================
    # =========================================================================

    async def do_next(self) -> None:
        if self.is_playing or self.waiting:
            return

        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.end_votes.clear()

        if -1 <= self.track_position < len(self.queue) - 1:
            self.last_played_position = self.track_position
            self.track_position += 1

            await self.play(self.queue[self.track_position])
            self.waiting = False

            await self.invoke_controller()
        else:
            print("finish")
            await self.terminate()

    # =========================================================================

    async def invoke_controller(self, force: bool = False) -> None:
        if self.updating:
            return

        self.updating = True

        if self.controller_view:
            self.controller_view.stop()

        if not self.controller:
            self.controller_view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            self.controller = await self.context.send(
                embed=self.controller_view.build_embed(),
                view=self.controller_view,
            )

        elif force or not await self.is_position_fresh():
            try:
                await self.controller.delete()
            except discord.HTTPException:
                pass

            self.controller_view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            self.controller = await self.context.send(
                embed=self.controller_view.build_embed(),
                view=self.controller_view,
            )

        else:
            self.controller_view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            await self.controller.edit(
                embed=self.controller_view.build_embed(),
                view=self.controller_view,
            )

        self.updating = False

    # =========================================================================

    async def is_position_fresh(self) -> bool:
        if not self.controller:
            return False

        try:
            async for message in self.context.channel.history(limit=5):
                if (
                    isinstance(message, discord.Message)
                    and message.id == self.controller.id
                ):
                    return True
        except (discord.HTTPException, AttributeError):
            return False

        return False

    # =========================================================================

    async def terminate(self) -> None:
        try:
            if self.controller:
                await self.controller.delete()
        except discord.HTTPException:
            pass

        try:
            await self.destroy()
        except KeyError:
            pass

    # =========================================================================

    def is_privileged(self, user: discord.Member) -> bool:
        return self.dj == user or user.guild_permissions.kick_members

    # =========================================================================

    def required(self, stop: bool = False) -> int:
        channel = self.bot.get_channel(
            int(self.channel_id if self.channel_id else 0)
        )
        if not isinstance(
            channel, (discord.VoiceChannel, discord.StageChannel)
        ):
            return -1

        required = math.ceil((len(channel.members) - 1) / 2.5)

        if stop and len(channel.members) == 3:
            required = 2

        return required

    # =========================================================================

    async def back_queue(self) -> None:
        self.track_position = self.last_played_position - 1
        self.last_played_position -= 1

        await self.stop()

    async def skip_queue(self) -> None:
        await self.stop()

    async def jump_queue(self, track: Track) -> None:
        try:
            self.track_position = self.queue.index(track) - 1
            self.last_played_position = self.track_position - 1

            await self.stop()
        except ValueError:
            pass

    async def remove_queue(self, track: Track) -> None:
        try:
            index = self.queue.index(track)
            del self.queue[self.queue.index(track)]

            if index == self.track_position:
                self.last_played_position -= 1
                self.track_position -= 1
                await self.stop()
        except ValueError:
            pass


def check_track_or_raise(track: Track):
    if track.length > 3605 * 2 * 1000:

        def _(x):
            return x

        raise TrackTooLong(_("The music should not exceed 2 hours"))
