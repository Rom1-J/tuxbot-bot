from typing import Union

import discord
import bcrypt
from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts
from .utils.models import Poll
from .utils import emotes as utils_emotes


class Polls(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    def get_poll(self, pld) -> Union[bool, Poll]:
        if pld.user_id != self.bot.user.id:
            poll = self.bot.engine \
                .query(Poll) \
                .filter(Poll.message_id == pld.message_id) \
                .one_or_none()

            if poll is not None:
                emotes = utils_emotes.get(len(poll.responses))

                if pld.emoji.name in emotes:
                    return poll

        return False

    async def remove_reaction(self, pld):
        channel: discord.TextChannel = self.bot.get_channel(
            pld.channel_id
        )
        message: discord.Message = await channel.fetch_message(
            pld.message_id
        )
        user: discord.User = await self.bot.fetch_user(pld.user_id)

        await message.remove_reaction(pld.emoji.name, user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pld: discord.RawReactionActionEvent):
        poll = self.get_poll(pld)

        if poll:
            if poll.is_anonymous:
                await self.remove_reaction(pld)

            user_id = str(pld.user_id).encode()
            responses = poll.responses

            choice = utils_emotes.get_index(pld.emoji.name) + 1
            responders = responses.get(str(choice))

            if not responders:
                print(responders, 'before0')
                user_id_hash = bcrypt.hashpw(user_id, bcrypt.gensalt())
                responders.append(user_id_hash)
                print(responders, 'after0')
            else:
                for i, responder in enumerate(responders):
                    if bcrypt.checkpw(user_id, responder.encode()):
                        print(responders, 'before1')
                        responders.pop(i)
                        print(responders, 'after1')
                    else:
                        print(responders, 'before2')
                        user_id_hash = bcrypt.hashpw(user_id, bcrypt.gensalt())
                        responders.append(user_id_hash)
                        print(responders, 'after2')

            poll.responses = responses
            print(poll.responses)
            self.bot.engine.commit()

            return 1

    """---------------------------------------------------------------------"""

    async def make_poll(self, ctx: commands.Context, poll: str, anonymous):
        question = (poll.split('|')[0]).strip()
        responses = [response.strip() for response in poll.split('|')[1:]]
        responses_row = {}
        emotes = utils_emotes.get(len(responses))

        stmt = await ctx.send(Texts('poll', ctx).get('**Preparation...**'))

        poll_row = Poll()
        self.bot.engine.add(poll_row)
        self.bot.engine.flush()

        e = discord.Embed(description=f"**{question}**")
        e.set_author(
            name=ctx.author,
            icon_url='https://cdn.pixabay.com/photo/2017/05/15/23/48/survey-2316468_960_720.png'
        )
        for i, response in enumerate(responses):
            responses_row[str(i+1)] = []
            e.add_field(
                name=f"{emotes[i]} __{response.capitalize()}__",
                value="**0** vote"
            )
        e.set_footer(text=f"ID: {poll_row.id}")

        poll_row.message_id = stmt.id
        poll_row.poll = e.to_dict()
        poll_row.is_anonymous = anonymous
        poll_row.responses = responses_row

        self.bot.engine.commit()

        await stmt.edit(content='', embed=e)
        for emote in range(len(responses)):
            await stmt.add_reaction(emotes[emote])

    @commands.group(name='sondage', aliases=['poll'])
    async def _poll(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            ...

    @_poll.group(name='create', aliases=['new', 'nouveau'])
    async def _poll_create(self, ctx: commands.Context, *, poll: str):
        is_anonymous = '--anonyme' in poll
        poll = poll.replace('--anonyme', '')

        await self.make_poll(ctx, poll, anonymous=is_anonymous)


def setup(bot: TuxBot):
    bot.add_cog(Polls(bot))
