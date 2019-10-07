import json
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
            poll = self.bot.database.session \
                .query(Poll) \
                .filter(Poll.message_id == pld.message_id)

            if poll.count() != 0:
                poll = poll.one()
                emotes = utils_emotes.get(len(poll.responses))

                if pld.emoji.name in emotes:
                    return poll

        return False

    async def remove_reaction(self, pld):
        channel: discord.TextChannel = self.bot.get_channel(pld.channel_id)
        message: discord.Message = await channel.fetch_message(pld.message_id)
        user: discord.User = await self.bot.fetch_user(pld.user_id)

        await message.remove_reaction(pld.emoji.name, user)

    async def update_poll(self, poll_id: int):
        poll = self.bot.database.session \
            .query(Poll) \
            .filter(Poll.id == poll_id) \
            .one()
        channel: discord.TextChannel = self.bot.get_channel(poll.channel_id)
        message: discord.Message = await channel.fetch_message(poll.message_id)

        content = json.loads(poll.content) \
            if isinstance(poll.content, str) \
            else poll.content
        responses = json.loads(poll.responses) \
            if isinstance(poll.responses, str) \
            else poll.responses

        for i, field in enumerate(content.get('fields')):
            responders = len(responses.get(str(i + 1)))
            if responders <= 1:
                field['value'] = f"**{responders}** vote"
            else:
                field['value'] = f"**{responders}** votes"

        e = discord.Embed(description=content.get('description'))
        e.set_author(
            name=content.get('author').get('name'),
            icon_url=content.get('author').get('icon_url')
        )
        for field in content.get('fields'):
            e.add_field(
                name=field.get('name'),
                value=field.get('value'),
                inline=True
            )
        e.set_footer(text=content.get('footer').get('text'))

        await message.edit(embed=e)

        poll.content = json.dumps(content)
        self.bot.database.session.commit()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pld: discord.RawReactionActionEvent):
        poll = self.get_poll(pld)

        if poll:
            if poll.is_anonymous:
                try:
                    await self.remove_reaction(pld)
                except discord.errors.Forbidden:
                    pass

            user_id = str(pld.user_id).encode()

            choice = utils_emotes.get_index(pld.emoji.name) + 1
            responses = json.loads(poll.responses) \
                if isinstance(poll.responses, str) \
                else poll.responses

            if not responses.get(str(choice)):
                user_id_hash = bcrypt.hashpw(user_id, bcrypt.gensalt())
                responses \
                    .get(str(choice)) \
                    .append(user_id_hash.decode())
            else:
                for i, responder in enumerate(responses.get(str(choice))):
                    if bcrypt.checkpw(user_id, responder.encode()):
                        responses \
                            .get(str(choice)) \
                            .pop(i)
                        break
                    else:
                        user_id_hash = bcrypt.hashpw(user_id, bcrypt.gensalt())
                        responses \
                            .get(str(choice)) \
                            .append(user_id_hash.decode())
                        break

            poll.responses = json.dumps(responses)
            self.bot.database.session.commit()
            await self.update_poll(poll.id)

    """---------------------------------------------------------------------"""

    async def make_poll(self, ctx: commands.Context, poll: str, anonymous):
        question = (poll.split('|')[0]).strip()
        responses = [response.strip() for response in poll.split('|')[1:]]
        responses_row = {}
        emotes = utils_emotes.get(len(responses))

        stmt = await ctx.send(Texts('poll', ctx).get('**Preparation...**'))

        poll_row = Poll()
        self.bot.database.session.add(poll_row)
        self.bot.database.session.flush()

        e = discord.Embed(description=f"**{question}**")
        e.set_author(
            name=self.bot.user if anonymous else ctx.author,
            icon_url="https://cdn.gnous.eu/tuxbot/survey1.png"
        )
        for i, response in enumerate(responses):
            responses_row[str(i + 1)] = []
            e.add_field(
                name=f"{emotes[i]} __{response.capitalize()}__",
                value="**0** vote"
            )
        e.set_footer(text=f"ID: {poll_row.id}")

        poll_row.message_id = stmt.id
        poll_row.channel_id = stmt.channel.id
        poll_row.content = e.to_dict()
        poll_row.is_anonymous = anonymous
        poll_row.responses = responses_row

        self.bot.database.session.commit()

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
