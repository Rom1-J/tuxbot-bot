import logging

import discord
from aiohttp import web
from discord.ext import commands

from bot import TuxBot

log = logging.getLogger(__name__)


class API(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot
        self.site = web.TCPSite

        app = web.Application()
        app.add_routes([web.get('/users/{user_id}', self.users)])

        self.runner = web.AppRunner(app)
        self.bot.loop.create_task(self.start_HTTPMonitoring_server())

    async def start_HTTPMonitoring_server(self):
        host = self.bot.config.get('API', 'Host')
        port = self.bot.config.get('API', 'Port')

        print(f"Starting API server on {host}:{port}")

        await self.runner.setup()
        self.site = web.TCPSite(self.runner, host, port)
        await self.site.start()

    async def users(self, request):
        try:
            user = await self.bot.fetch_user(request.match_info['user_id'])
        except discord.NotFound:
            return web.Response(status=404)

        json = {
            'id': user.id,
            'username': user.name,
            'discriminator': user.discriminator,
            'avatar': user.avatar,
            'default_avatar': user.default_avatar.value,
            'bot': user.bot,
            'system': user.system,
        }

        return web.json_response(
            json
        )


def setup(bot: TuxBot):
    bot.add_cog(API(bot))
