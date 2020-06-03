import logging
from io import BytesIO

import discord
from discord.ext import commands, flags

from app import TuxBot
from utils.functions.extra import ContextPlus, command_extra

log = logging.getLogger(__name__)


class Images(commands.Cog, name="Images"):
    def __init__(self, bot):
        self.bot = bot
        self.image_api = "http://0.0.0.0:8080"

    async def _send_meme(self, ctx: ContextPlus, endpoint: str, **passed_flags):
        async with ctx.typing():
            url = f"{self.image_api}/{endpoint}?"
            for key, val in passed_flags.items():
                if val:
                    url += f"{key}={val}&"

            async with self.bot.session.get(url) as r:
                if r.status != 200:
                    return await ctx.send("Failed...")

                data = BytesIO(await r.read())

        await ctx.send(
            file=discord.File(data, "output.png")
        )

    @command_extra(name="phcomment")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _phcomment(self, ctx: ContextPlus, user: discord.User = None, *, message: commands.clean_content(fix_channel_mentions=True, escape_markdown=True)):
        async with ctx.typing():
            message = message.replace("&", "%26")
            if user is None:
                avatar = ctx.author.avatar_url_as(format='png')
                username = ctx.author.name
            else:
                avatar = user.avatar_url_as(format='png')
                username = user.name

            url = f"{self.image_api}/ph/comment" \
                  f"?image={avatar}" \
                  f"&username={username}" \
                  f"&message={message}"

            async with self.bot.session.get(url) as r:
                if r.status != 200:
                    return await ctx.send("Failed...")

                data = BytesIO(await r.read())

        await ctx.send(
            file=discord.File(data, "output.png")
        )

    @command_extra(name="phvideo")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _phvideo(self, ctx: ContextPlus, image: str, author: discord.User, *, title: commands.clean_content(fix_channel_mentions=True, escape_markdown=True)):
        async with ctx.typing():
            url = f"{self.image_api}/ph/video" \
                  f"?image={image}" \
                  f"&username={author.name}" \
                  f"&title={title}"

            async with self.bot.session.get(url) as r:
                if r.status != 200:
                    return await ctx.send("Failed...")

                data = BytesIO(await r.read())

        await ctx.send(
            file=discord.File(data, "output.png")
        )

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @flags.add_flag("--text3", type=str)
    @command_extra(name="balloon")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _balloon(self, ctx: ContextPlus, **passed_flags):
        passed_flags["text3"] = passed_flags.get("text3")
        passed_flags["text4"] = passed_flags.get("text1")
        passed_flags["text5"] = passed_flags.get("text2")

        await self._send_meme(ctx, 'balloon', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @flags.add_flag("--text3", type=str)
    @command_extra(name="butterfly")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _butterfly(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'butterfly', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @command_extra(name="buttons")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _buttons(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'buttons', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @command_extra(name="cmm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _cmm(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'change_my_mind', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @command_extra(name="drake")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _drake(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'drake', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str, default=False)
    @command_extra(name="fry")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _fry(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'fry', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str, default=False)
    @command_extra(name="imagination")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _imagination(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'imagination', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str, default=False)
    @command_extra(name="everywhere")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _everywhere(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'everywhere', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @flags.add_flag("--text3", type=str)
    @command_extra(name="choice")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _choice(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'choice', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @command_extra(name="pika")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _pika(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'pika', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @flags.add_flag("--text3", type=str)
    @command_extra(name="pkp")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _pkp(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'pkp', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @flags.add_flag("--text2", type=str)
    @command_extra(name="puppet")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _puppet(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'puppet', **passed_flags)

    @flags.add_flag("--text1", type=str)
    @command_extra(name="scroll_of_truth", alias=['sot'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _sot(self, ctx: ContextPlus, **passed_flags):
        await self._send_meme(ctx, 'scroll_of_truth', **passed_flags)
