import logging
import socket
import ipinfo
import discord

from discord.ext import commands, flags
from ipwhois import Net
from ipwhois.asn import IPASN
from ipinfo.exceptions import RequestQuotaExceededError
from requests.exceptions import HTTPError

from app import TuxBot
from utils.functions.extra import ContextPlus, command_extra

log = logging.getLogger(__name__)


class Network(commands.Cog, name="Useless"):
    def __init__(self, bot: TuxBot):
        self.bot = bot

    @flags.add_flag("-i", "--ip", type=str, default='v4',
                    choices=['v4', '4', 'v6', '6'])
    @command_extra(name="iplocalise", aliases=['localiseip'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _iplocalise(self, ctx: ContextPlus, target: str, **passed_flags):
        loading = await ctx.send(
            "_Récupération des informations..._", deletable=False
        )

        def get_hostname(dtl, tgt):
            try:
                return dtl.hostname
            except AttributeError:
                try:
                    return socket.gethostbyaddr(tgt)[0]
                except (ValueError, socket.herror):
                    return 'N/A'

        ip_type = passed_flags.get('ip')
        target_copy = target

        # clean https://, last /, ...
        spltTgt = target.split("://")
        target = spltTgt[
            (0, 1)[len(spltTgt) > 1]
        ].split("?")[0].split('/')[0].split(':')[0].lower()

        try:
            target = socket.getaddrinfo(
                target, None,
                socket.AF_INET if ip_type in ['v4', '4'] else socket.AF_INET6
            )[1][4][0]
        except socket.gaierror:
            return \
                await ctx.send("Erreur, cette adresse n'est pas disponible.")

        net = Net(target)
        obj = IPASN(net)
        ip_info = obj.lookup()

        try:
            handler = ipinfo.getHandler(self.bot._config.ipinfo)
            details = handler.getDetails(target)
            api_result = True
        except (RequestQuotaExceededError, HTTPError):
            details = None
            api_result = False

        if api_result:
            belongs = f"{details.org}"

            osm = f"https://www.openstreetmap.org/" \
                  f"?mlat={details.latitude}" \
                  f"&mlon={details.longitude}" \
                  f"#map=5/{details.latitude}/{details.longitude}" \
                  f"&layers=H"

            region = f"[{details.city} - {details.region} " \
                     f"({details.country})]({osm})"
            flag = f"https://www.countryflags.io/" \
                   f"{details.country}/shiny/64.png"
        else:
            belongs = f"{ip_info['asn_description']} (AS{ip_info['asn']})"
            region = f"{ip_info['asn_country_code']}"
            flag = f"https://www.countryflags.io/" \
                   f"{ip_info['asn_country_code']}/shiny/64.png"

        e = discord.Embed(
            title=f"**Information sur __{target_copy}__ :**"
                  f" `{target}`",
            color=0x5858d7
        )

        e.add_field(name="Appartient à :", value=belongs)
        e.add_field(name="RIR :", value=f"{ip_info['asn_registry']}")
        e.add_field(name="Region :", value=region)

        e.add_field(name="Nom de l'hôte :",
                    value=get_hostname(details, target), inline=False)

        e.set_thumbnail(url=flag)

        await loading.delete()
        await ctx.send(embed=e)


def setup(bot: TuxBot):
    cog = Network(bot)
    bot.add_cog(cog)
