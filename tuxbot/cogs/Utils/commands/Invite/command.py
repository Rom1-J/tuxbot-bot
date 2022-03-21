"""
tuxbot.cogs.Utils.commands.Invite.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives tuxbot invite links
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class InviteCommand(commands.Cog):
    """Gives tuxbot invite links"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="invite")
    async def _invite(self, ctx: commands.Context):
        basic_perms = discord.Permissions(
            add_reactions=True,
            read_messages=True,
            send_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            connect=True,
            speak=True,
            manage_roles=True,
        )

        admin_perms = discord.Permissions(
            create_instant_invite=True,
            kick_members=True,
            ban_members=True,
            add_reactions=True,
            read_messages=True,
            send_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            connect=True,
            speak=True,
            manage_roles=True,
        )

        e = discord.Embed(
            title="Invite", color=self.bot.utils.colors.EMBED_BORDER.value
        )

        e.add_field(
            name="Minimal",
            value=(
                "The minimum permissions include the strict requirements for "
                "the proper functioning of all basics commands.\n"
                "[Add!]"
                "({})".format(
                    discord.utils.oauth_url(
                        self.bot.user.id, permissions=basic_perms
                    )
                )
            ),
            inline=False,
        )
        e.add_field(
            name="Admin",
            value=(
                "All minimal permissions + extra permissions for admin "
                "commands such as kick and ban\n"
                "[Add!]"
                "({})".format(
                    discord.utils.oauth_url(
                        self.bot.user.id, permissions=admin_perms
                    )
                )
            ),
            inline=False,
        )

        await ctx.send(embed=e)
