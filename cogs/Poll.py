import json
import logging
from typing import Union

import discord
from discord.ext import commands
from yarl import URL

from bot import TuxBot
from utils import PollModel, ResponsesModel
from utils import Texts
from utils.functions import emotes as utils_emotes
from utils import group_extra

log = logging.getLogger(__name__)


class Poll(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot
        self.icon = ":bar_chart:"
        self.big_icon = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/233/bar-chart_1f4ca.png:"

    def get_poll(self, pld) -> Union[bool, PollModel]:
        if pld.user_id != self.bot.user.id:
            poll = self.bot.database.session \
                .query(PollModel) \
                .filter(PollModel.message_id == pld.message_id)

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

            responses = self.bot.database.session.query(ResponsesModel) \
                .filter(
                ResponsesModel.poll_id == poll.id,
                ResponsesModel.user == pld.user_id,
                ResponsesModel.choice == choice
            )

            if responses.count() != 0:
                response = responses.first()
                self.bot.database.session.delete(response)
                self.bot.database.session.commit()
            else:
                response = ResponsesModel(
                    user=pld.user_id,
                    poll_id=poll.id,
                    choice=choice
                )
                self.bot.database.session.add(response)
                self.bot.database.session.commit()

            await self.update_poll(poll.id)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,
                                     pld: discord.RawReactionActionEvent):
        poll = self.get_poll(pld)

        if poll:
            choice = utils_emotes.get_index(pld.emoji.name)

            responses = self.bot.database.session.query(ResponsesModel) \
                .filter(
                ResponsesModel.poll_id == poll.id,
                ResponsesModel.user == pld.user_id,
                ResponsesModel.choice == choice
            )

            if responses.count() != 0:
                response = responses.first()
                self.bot.database.session.delete(response)
                self.bot.database.session.commit()
            await self.update_poll(poll.id)

    ###########################################################################

    async def create_poll(self, ctx: commands.Context, poll: str, anonymous):
        question = (poll.split('|')[0]).strip()
        responses = [response.strip() for response in poll.split('|')[1:]]
        emotes = utils_emotes.get(len(responses))

        stmt = await ctx.send(Texts('poll', ctx).get('**Preparation...**'))

        poll_row = PollModel()
        self.bot.database.session.add(poll_row)
        self.bot.database.session.flush()

        e = discord.Embed(description=f"**{question}**")
        e.set_author(
            name=ctx.author,
            icon_url="https://cdn.gnous.eu/tuxbot/survey1.png"
        )
        for i, response in enumerate(responses):
            e.add_field(
                name=f"__{emotes[i]}` - {response.capitalize()}`__",
                value="**0** vote"
            )
        e.set_footer(text=f"ID: #{poll_row.id}")

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
            .query(PollModel) \
            .filter(PollModel.id == poll_id) \
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
        raw_responses = self.bot.database.session \
            .query(ResponsesModel) \
            .filter(ResponsesModel.poll_id == poll_id)
        responses = {}

        for response in raw_responses.all():
            if responses.get(response.choice):
                responses[response.choice] += 1
            else:
                responses[response.choice] = 1

        for i, field in enumerate(content.get('fields')):
            responders = responses.get(i, 0)
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

    @group_extra(name='poll', aliases=['sondage'], category='poll')
    async def _poll(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help('poll')

    @_poll.group(name='create', aliases=['new', 'nouveau'])
    async def _poll_create(self, ctx: commands.Context, *, poll: str):
        is_anonymous = '--anonyme' in poll
        poll = poll.replace('--anonyme', '')

        await self.create_poll(ctx, poll, anonymous=is_anonymous)


def setup(bot: TuxBot):
    bot.add_cog(Poll(bot))
