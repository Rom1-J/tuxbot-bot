import json
from typing import Union

import discord
from discord.ext import commands
from yarl import URL

from bot import TuxBot
from .utils.lang import Texts
from .utils.models import Poll, Responses
from .utils import emotes as utils_emotes


class Polls(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    def get_poll(self, pld) -> Union[bool, Poll]:
        if pld.user_id != self.bot.user.id:
            poll = self.bot.database.session \
                .query(Poll) \
                .filter(Poll.message_id == pld.message_id)

            if poll.count() > 0:
                poll = poll.one()
                emotes = utils_emotes.get(poll.available_choices)
                if pld.emoji.name in emotes:
                    return poll

        return False

    async def remove_reaction(self, pld):
        channel: discord.TextChannel = self.bot.get_channel(pld.channel_id)
        message: discord.Message = await channel.fetch_message(pld.message_id)
        user: discord.User = await self.bot.fetch_user(pld.user_id)

        await message.remove_reaction(pld.emoji.name, user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pld: discord.RawReactionActionEvent):
        poll = self.get_poll(pld)

        if poll:
            if poll.is_anonymous:
                try:
                    await self.remove_reaction(pld)
                except discord.errors.Forbidden:
                    pass
            choice = utils_emotes.get_index(pld.emoji.name)

            print(choice)

            response = self.bot.database.session.query(Poll) \
                .filter(
                Responses.poll_id == poll.id,
                Responses.user == pld.user_id,
                Responses.choice == choice
            )

            if response.count() != 0:
                print("--pre delete--")
                response = response.one()
                self.bot.database.session.delete(response)
                print("--post delete--")
            else:
                print("--pre add--")
                response = Responses(
                    user=pld.user_id,
                    poll_id=poll.id,
                    choice=choice
                )
                self.bot.database.session.add(response)
                print("--post add--")
            self.bot.database.session.commit()

    """---------------------------------------------------------------------"""

    async def create_poll(self, ctx: commands.Context, poll: str, anonymous):
        question = (poll.split('|')[0]).strip()
        responses = [response.strip() for response in poll.split('|')[1:]]
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
            e.add_field(
                name=f"{emotes[i]} __{response.capitalize()}__",
                value="**0** vote"
            )
        e.set_footer(text=f"ID: {poll_row.id}")

        poll_row.channel_id = stmt.channel.id
        poll_row.message_id = stmt.id
        poll_row.content = e.to_dict()
        poll_row.is_anonymous = anonymous
        poll_row.available_choices = len(responses)

        self.bot.database.session.commit()

        await stmt.edit(content='', embed=e)
        for emote in range(len(responses)):
            await stmt.add_reaction(emotes[emote])

    async def update_poll(self, poll_id: int):
        poll = self.bot.database.session \
            .query(Poll) \
            .filter(Poll.id == poll_id) \
            .one()
        channel: discord.TextChannel = self.bot.get_channel(poll.channel_id)
        message: discord.Message = await channel.fetch_message(poll.message_id)

        chart_base_url = "https://quickchart.io/chart?backgroundColor=white&c="
        chart_options = {
            'type': 'pie',
            'data': {
                'labels': [],
                'datasets': [
                    {
                        'data': []
                    }
                ]
            }
        }

        content = json.loads(poll.content) \
            if isinstance(poll.content, str) \
            else poll.content
        responses = json.loads(poll.responses) \
            if isinstance(poll.responses, str) \
            else poll.responses

        for i, field in enumerate(content.get('fields')):
            responders = len(responses.get(str(i + 1)))
            chart_options.get('data') \
                .get('labels') \
                .append(field.get('name')[5:].replace('__', ''))
            chart_options.get('data') \
                .get('datasets')[0] \
                .get('data') \
                .append(responders)

            if responders <= 1:
                field['value'] = f"**{responders}** vote"
            else:
                field['value'] = f"**{responders}** votes"

        e = discord.Embed(description=content.get('description'))
        e.set_author(
            name=content.get('author').get('name'),
            icon_url=content.get('author').get('icon_url')
        )
        chart_url = URL(chart_base_url + json.dumps(chart_options))
        e.set_thumbnail(url=str(chart_url))
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

    @commands.group(name='sondage', aliases=['poll'])
    async def _poll(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            ...

    @_poll.group(name='create', aliases=['new', 'nouveau'])
    async def _poll_create(self, ctx: commands.Context, *, poll: str):
        is_anonymous = '--anonyme' in poll
        poll = poll.replace('--anonyme', '')

        await self.create_poll(ctx, poll, anonymous=is_anonymous)


def setup(bot: TuxBot):
    bot.add_cog(Polls(bot))
