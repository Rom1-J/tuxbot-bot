import time

import discord
from tuxbot.cogs.Mod.models import AutoBan


# pylint: disable=unused-argument
async def on_member_join(self, member: discord.Member):
    if time.time() - member.created_at.timestamp() > 2592000:
        return

    autobans = await AutoBan.filter(server_id=member.guild.id).all()

    for autoban in autobans:
        if autoban.match.lower() in member.name.lower():
            await member.send(autoban.reason)
            await member.ban(reason=autoban.reason, delete_message_days=1)

            if autoban.log_channel:
                try:
                    channel = await member.guild.fetch_channel(autoban.log_channel)

                    await channel.send(
                        f"Autoban: {member}\n"
                        f"For matching with: {autoban.match}"
                    )
                except Exception:
                    pass
