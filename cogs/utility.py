import datetime
import json
import pytz
import random
import urllib
import aiohttp
import ipinfo as ipinfoio

import pydig

import telnetlib
from graphviz import Digraph

from ipwhois.net import Net
from ipwhois.asn import IPASN
import ipwhois

import discord
import requests, re
from discord.ext import commands
import socket

class Utility(commands.Cog):
    """Commandes utilitaires."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="clock", pass_context=True, case_insensitive=True)
    async def clock(self, ctx):
        """Display hour in a country"""

        if ctx.invoked_subcommand is None:
            text = open('texts/clocks.md').read()
            em = discord.Embed(title='Liste des Horloges', description=text, colour=0xEEEEEE)
            await ctx.send(embed=em)

    @clock.command(name="montréal", aliases=["mtl", "montreal"], pass_context=True)
    async def clock_montreal(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('America/Montreal'))
        site = "http://ville.montreal.qc.ca/"
        img = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Rentier_fws_1.jpg"
        country = "au Canada, Québec"
        description = "Montréal est la deuxième ville la plus peuplée du Canada. Elle se situe dans la région du Québec"

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Montréal', description=f"A [Montréal]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)

    @clock.command(name="vancouver", pass_context=True)
    async def clock_vancouver(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('America/Vancouver'))
        site = "http://vancouver.ca/"
        img = "https://upload.wikimedia.org/wikipedia/commons/f/fe/Dock_Vancouver.JPG"
        country = "au Canada"
        description = "Vancouver, officiellement City of Vancouver, est une cité portuaire au Canada"

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Vancouver', description=f"A [Vancouver]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)

    @clock.command(name="new-york",aliases=["ny", "n-y", "new york"], pass_context=True)
    async def clock_new_york(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('America/New_York'))
        site = "http://www1.nyc.gov/"
        img = "https://upload.wikimedia.org/wikipedia/commons/e/e3/NewYork_LibertyStatue.jpg"
        country = "aux U.S.A."
        description = "New York, est la plus grande ville des États-Unis en termes d'habitants et l'une des plus importantes du continent américain. "

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à New York', description=f"A [str(New York]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)
            
    @clock.command(name="la", aliases=["los-angeles", "losangeles", "l-a", "los angeles"], pass_context=True)
    async def clock_la(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('America/Los_Angeles'))
        site = "https://www.lacity.org/"
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/800px-LA_Skyline_Mountains2.jpg"
        country = "aux U.S.A."
        description = "Los Angeles est la deuxième ville la plus peuplée des États-Unis après New York. Elle est située dans le sud de l'État de Californie, sur la côte pacifique."

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Los Angeles', description=f"A [Los Angeles]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)
            
    @clock.command(name="paris", aliases=["baguette"],pass_context=True)
    async def clock_paris(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('Europe/Paris'))
        site = "http://www.paris.fr/"
        img = "https://upload.wikimedia.org/wikipedia/commons/a/af/Tour_eiffel_at_sunrise_from_the_trocadero.jpg"
        country = "en France"
        description = "Paris est la capitale de la France. Elle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien."

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Paris', description=f"A [Paris]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)
    
    @clock.command(name="berlin", pass_context=True)
    async def clock_berlin(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('Europe/Berlin'))
        site = "http://www.berlin.de/"
        img = "https://upload.wikimedia.org/wikipedia/commons/9/91/Eduard_Gaertner_Schlossfreiheit.jpg"
        country = "en Allemagne"
        description = "Berlin est la capitale et la plus grande ville d'Allemagne. Située dans le nord-est du pays, elle compte environ 3,5 millions d'habitants. "

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Berlin', description=f"A [Berlin]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)
    
    @clock.command(name="berne", aliases=["zurich", "bern"], pass_context=True)
    async def clock_berne(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('Europe/Zurich'))
        site = "http://www.berne.ch/"
        img = "https://upload.wikimedia.org/wikipedia/commons/d/db/Justitia_Statue_02.jpg"
        country = "en Suisse"
        description = "Berne est la cinquième plus grande ville de Suisse et la capitale du canton homonyme. Depuis 1848, Berne est la « ville fédérale »."

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Berne', description=f"A [Berne]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)
    
    @clock.command(name="tokyo", pass_context=True)
    async def clock_tokyo(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('Asia/Tokyo'))
        site = "http://www.gotokyo.org/"
        img = "https://upload.wikimedia.org/wikipedia/commons/3/37/TaroTokyo20110213-TokyoTower-01.jpg"
        country = "au Japon"
        description = "Tokyo, anciennement Edo, officiellement la préfecture métropolitaine de Tokyo, est la capitale du Japon."

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Tokyo', description=f"A [Tokyo]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)
    
    @clock.command(name="moscou", aliases=["moscow", "moskova"], pass_context=True)
    async def clock_moscou(self, ctx):
        then = datetime.datetime.now(pytz.utc)

        utc = then.astimezone(pytz.timezone('Europe/Moscow'))
        site = "https://www.mos.ru/"
        img = "https://upload.wikimedia.org/wikipedia/commons/f/f7/Andreyevsky_Zal.jpg"
        country = "en Russie"
        description = "Moscou est la capitale de la Fédération de Russie et la plus grande ville d'Europe. Moscou est situé sur la rivière Moskova. "

        form = '%H heures %M'
        tt = utc.strftime(form)

        em = discord.Embed(title='Heure à Moscou', description=f"A [Moscou]({site}) {country}, Il est **{str(tt)}** ! \n {description} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_", colour=0xEEEEEE)
        em.set_thumbnail(url = img)
        await ctx.send(embed=em)

    """---------------------------------------------------------------------"""

    @commands.command()
    async def ytdiscover(self, ctx):
        """Random youtube channel"""
        with open('texts/ytb.json') as js:
            ytb = json.load(js)

        clef = str(random.randint(0,12))
        chaine = ytb["{}".format(clef)]

        embed = discord.Embed(title=chaine['name'], 
            url=chaine['url'], 
            description=f"**{chaine['name']}**, {chaine['desc']} \n[Je veux voir ça]({chaine['url']})")
        embed.set_thumbnail(url='https://outout.tech/tuxbot/yt.png')
        await ctx.send(embed=embed)

    """---------------------------------------------------------------------"""

    @commands.command(name='iplocalise', pass_context=True)
    async def _iplocalise(self, ctx, ipaddress, iptype=""):
        realipaddress = ipaddress
        """Getting headers."""
        if ipaddress.startswith("http://"):
            if ipaddress[-1:] == '/':
                ipaddress = ipaddress[:-1]
            ipaddress = ipaddress.split("http://")[1]
        if ipaddress.startswith("https://"):
            if ipaddress[-1:] == '/':
                ipaddress = ipaddress[:-1]
            ipaddress = ipaddress.split("https://")[1]
        
        if(iptype=="ipv6" or iptype=="v6" or iptype=="-6"):
            try:
                ipaddress = socket.getaddrinfo(ipaddress, None, socket.AF_INET6)[1][4][0]
            except Exception as e:
                await ctx.send("Erreur, cette adresse n'est pas disponible en IPv6.")
                return
        elif(iptype=="ipv4" or iptype=="v4" or iptype=="-4"):
            try:
                ipaddress = socket.getaddrinfo(ipaddress, None, socket.AF_INET)[1][4][0]
            except Exception as e:
                await ctx.send("Erreur, cette adresse n'est pas disponible en IPv4.")
                return
        else:
            try:
                ipaddress = socket.getaddrinfo(ipaddress, None)[1][4][0]
            except Exception as e:
                await ctx.send("Erreur, cette adresse n'est pas disponible.")
                return

        iploading = await ctx.send("_Récupération des informations..._")

        try:
            net = Net(ipaddress)
            obj = IPASN(net)
            ipinfo = obj.lookup()
        except ipwhois.exceptions.IPDefinedError: 
            await ctx.send("Cette IP est reservée à un usage local selon la RFC 1918. Impossible d'avoir des informations supplémentaires à son propos.")
            await iploading.delete()
            return

        try:
            iphostname = socket.gethostbyaddr(ipaddress)[0]
        except:
            iphostname = "N/A"

        # IPINFO api
        api_result = True
        try:
            with open('ipinfoio.key') as k:
                access_token = k.read().replace("\n", "")
            handler = ipinfoio.getHandler(access_token)
            details = handler.getDetails(ipaddress)
        except Exception as e:
            api_result = False

        try:
            embed = discord.Embed(title=f"Informations pour ``{realipaddress} ({ipaddress})``", color=0x5858d7)
            
            if(api_result):
                asn = details.org.split(" ")[0]
                embed.add_field(name="Appartient à :", value=f"[{details.org}](https://bgp.he.net/{asn})")
            else:
                embed.add_field(name="Appartient à :", value=f"{ipinfo['asn_description']} ([AS{ipinfo['asn']}](https://bgp.he.net/{ipinfo['asn']}))", inline = False)
            
            embed.add_field(name="RIR :", value=f"{ipinfo['asn_registry']}", inline = True)
            
            if(api_result):
                embed.add_field(name="Région :", value=f"{details.city} - {details.region} ({details.country})")
            else:
                embed.add_field(name="Région :", value=f"{ipinfo['asn_country_code']}")
            embed.add_field(name="Nom de l'hôte :", value=f"{iphostname}")

            # Adding country flag 
            if(api_result):
                embed.set_thumbnail(url=f"https://www.countryflags.io/{details.country}/shiny/64.png")
            else:
                embed.set_thumbnail(url=f"https://www.countryflags.io/{ipinfo['asn_country_code']}/shiny/64.png")
            
            await ctx.send(embed=embed)
        except:
            await ctx.send(content=f"Erreur, impossible d'avoir des informations sur l'adresse IP ``{realipaddress}``")
        await iploading.delete()

    """---------------------------------------------------------------------"""
    @commands.command(name='dig', pass_context=True)
    async def _dig(self, ctx, domain, querytype="abc", dnssec="no"): 
        if not querytype in ['A', 'AAAA', 'CNAME', 'NS', 'DS', 'DNSKEY', 'SOA', 'TXT', 'PTR', 'MX']: 
            await ctx.send("Requêtes supportées : A, AAAA, CNAME, NS, DS, DNSKEY, SOA, TXT, PTR, MX")
            return

        if(dnssec == "no"):
            resolver = pydig.Resolver(
                nameservers=[
                    '80.67.169.40',
                    '80.67.169.12',
                ]
            )
        else: 
            resolver = pydig.Resolver(
                nameservers=[
                    '80.67.169.40',
                    '80.67.169.12',
                ],
                additional_args=[
                    '+dnssec',
                ]
            )

        resquery = resolver.query(domain, querytype)
        embed = discord.Embed(title=f"Requête DIG sur {domain} pour une entrée {querytype}", color=0x5858d7)
        
        champ_id = 1
        for champ in resquery:
            embed.add_field(name=f"Champ {champ_id} :", value=champ)
            champ_id = champ_id + 1 

        if champ_id == 1: 
            embed.add_field(name="Ooops", value="Pas de résultat")
        await ctx.send(embed=embed)


    """---------------------------------------------------------------------"""
    @commands.command(name='getheaders')
    async def _getheaders(self, ctx: commands.Context, addr: str):
        if (addr.startswith('http') or addr.startswith('ftp')) is not True:
           addr = f"http://{addr}"

        await ctx.trigger_typing()

        try:
            async with self.bot.session.get(addr) as s:
                e = discord.Embed(
                    title=f"Headers : {addr}",
                    color=0xd75858
                )
                e.add_field(name="Status", value=s.status, inline=True)
                e.set_thumbnail(url=f"https://http.cat/{s.status}")

                headers = dict(s.headers.items())
                headers.pop('Set-Cookie', headers)

                for key, value in headers.items():
                    e.add_field(name=key, value=value, inline=True)
                await ctx.send(embed=e)

        except aiohttp.ClientError:
            await ctx.send(
                f"Cannot connect to host {addr}"
            )


    """---------------------------------------------------------------------"""
    @commands.command(name='peeringdb', pass_context=True)
    async def _peeringdb(self, ctx, *, asn):
        def notEmptyField(embed, name, value):
            if(value != ""):
                embed.add_field(name=name, value=value)

        if asn.startswith("AS"):
            asn = asn[2:]
        loadingmsg = await ctx.send("_Récupération des informations..._")

        """Getting the ASN id in the peeringdb database"""
        try:
            asnid = urllib.request.urlopen("https://www.peeringdb.com/api/as_set/" + asn)
            asnid = json.loads(asnid.read().decode())
            pdbid = asnid["data"][0][asn]

            asinfo = urllib.request.urlopen("https://www.peeringdb.com/api/net?irr_as_set=" + pdbid)

            asinfo = json.loads(asinfo.read().decode())["data"]

            for asndata in asinfo:
                if(asndata['asn'] == int(asn)):
                    asinfo = asndata

            asproto = ""
            if(asinfo["info_ipv6"]):
                asproto = asproto + "IPv6 "
            if(asinfo["info_unicast"]):
                asproto = asproto + "Unicast "
            if(asinfo["info_multicast"]):
                asproto = asproto + "Multicast "
            if(asinfo["info_never_via_route_servers"]):
                asproto = asproto + "Never via Route servers"
            

            print(pdbid)

            embed = discord.Embed(title=f"Informations pour {asinfo['name']} ``AS{asn}``", color=0x5858d7)
            notEmptyField(embed, name="Nom :", value=asinfo['name'])
            notEmptyField(embed, name="Aka :", value=asinfo['aka'])
            notEmptyField(embed, name="Site :", value=asinfo['website'])
            notEmptyField(embed, name="Looking Glass :", value=asinfo['looking_glass'])
            notEmptyField(embed, name="Traffic :", value=asinfo['info_traffic'])
            notEmptyField(embed, name="Ratio du traffic :", value=asinfo['info_ratio'])
            notEmptyField(embed, name="Prefixes IPv4 :", value=asinfo['info_prefixes4'])
            notEmptyField(embed, name="Prefixes IPv6 :", value=asinfo['info_prefixes6'])
            notEmptyField(embed, name="Politique de Peering :", value=f"[{asinfo['policy_general']}]({asinfo['policy_url']})")
            notEmptyField(embed, name="Protocoles supportés :", value=asproto)
            embed.set_footer(text=f"https://www.peeringdb.com/")
            await ctx.send(embed=embed)
            await loadingmsg.delete()
        except IndexError:
            await ctx.send(f"Impossible d'avoir des informations sur l'AS AS{asn}")
            await loadingmsg.delete()
        except urllib.error.HTTPError:
            await ctx.send(f"L'AS{asn} est introuvable dans la base de données de PeeringDB.")
            await loadingmsg.delete()

    """---------------------------------------------------------------------"""
    @commands.command(name='shroute', pass_context=True)
    async def _shroute(self, ctx, srv, ipaddress):
        """Show as path graph to an IP via data from a Route Server using graphviz"""

        if not srv in ["opentransit", 'he', 'att', "oregonuniv", "warian", 'csaholdigs', 'iamageeknz']: 
            await ctx.send("Requêtes supportées : opentransit (Orange), he (Huricanne Electric), att (AT&T), oregonuniv, warian, csaholdigs, iamageeknz")
            return

        #List of RS 
        if srv == "opentransit": 
            host = "route-server.opentransit.net"
            user = "rviews"
            password = "Rviews"
            lg_asn = "5511"
            cmd = "show bgp {}"
        elif srv == "oregonuniv": 
            host = "route-views.routeviews.org"
            user = "rviews"
            password = "none"
            lg_asn = "3582"
            cmd = "show bgp {}"
        elif srv == "warian": 
            host = "route-server.warian.net"
            user = "none"
            password = "rviews"
            lg_asn = "56911"
            cmd = "show bgp ipv4 unicast {}"
        elif srv == "csaholdigs": #Blacklist sometime
            host = "route-views.sg.routeviews.org"
            user = "none"
            password = "none"
            lg_asn = "45494"
            cmd = "show bgp ipv4 unicast {}"
        elif srv == "he": #Blacklist sometime
            host = "route-server.he.net"
            user = "none"
            password = "none"
            lg_asn = "6939"
            cmd = "show bgp ipv4 unicast {}"
        elif srv == "iamageeknz": #Blacklist sometime
            host = "rs.as45186.net"
            user = "none"
            password = "none"
            lg_asn = "45186"
            cmd = "show bgp ipv4 unicast {}"    
        elif srv == "att": 
            host = "route-server.ip.att.net"
            user = "rviews"
            password = "rviews"
            lg_asn = "7018"
            cmd = "show route {}" 

        ip = ipaddress
        await ctx.send("Connexion en cours au route server...")
        tn = telnetlib.Telnet(host)

        #Login to the RS via Telnet 
        if user != "none":
            if(srv == "att"):
                tn.read_until("login: ".encode())
                tn.write((user + "\n").encode())
            else:
                tn.read_until("Username: ".encode())
                tn.write((user + "\n").encode())

        if password != "none":
            if(srv == "att"):
                tn.read_until("Password:".encode())
                tn.write((password + "\n").encode())
                print("ok")
            else: 
                tn.read_until("Password: ".encode())
                tn.write((password + "\n").encode())

        await ctx.send("Connecté ! Récupération des données...")

        #Sending show route via telnet to the RS
        tn.write((cmd + "\n").format(ip).encode())
        tn.write(chr(25).encode())
        tn.write(chr(25).encode())
        tn.write(chr(25).encode())
        tn.write("q\n".encode())
        tn.write("exit\n".encode())

        await ctx.send("Données récupérées ! Traitement en cours")

        #Parsing data
        data = tn.read_all().decode("utf-8")
        paths = {}

        #Parsing as paths
        paths["as_list"] = re.findall(r"  ([0-9][0-9 ]+),", data)
        if(paths["as_list"] == []):
            paths["as_list"] = re.findall(r"  ([0-9][0-9 ]+)[^0-9.]", data)

        #Custom parsing for AT&T 
        if(srv == "att"):
            paths["as_list"] = re.findall(r"(?<=AS path: 7018 )[0-9][0-9 ]+[^ I]", data)

        #Graphviz diagram
        g = Digraph('G', filename='bgpgraph', format='png', graph_attr={'rankdir':'LR', 'concentrate': 'true'})

        #Diagram paths generation
        as_path_count = 0
        for as_path in paths['as_list']: 
            as_path = as_path.split(" ")
            as_path.reverse()
            original_asn = as_path[0]
            border_asn = as_path[-1]
            precedent_asn = original_asn
            for asn in as_path:
                if asn != "2001": #Cause HE got a default or something weird to this asn 
                    if asn != original_asn: 
                        g.edge("AS" + asn, "AS" + precedent_asn)
                        precedent_asn = asn 
                    if asn == border_asn: 
                        g.edge("AS" + lg_asn, "AS" + asn)
                    as_path_count += 1
        
        #If empty as_path
        if as_path_count == 0: 
            await ctx.send("Pas de route trouvée vers l'IP demandée depuis le route server choisi.")
            return 

        #Render the graph
        g.render()

        #Send it
        with open('bgpgraph.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'bgpgraph.png'))

    """---------------------------------------------------------------------"""
    
    @commands.command(name='git', pass_context=True)
    async def _git(self, ctx):
        """Pour voir mon code"""
        text = "How tu veux voir mon repos Gitea pour me disséquer ? " \
               "Pas de soucis ! Je suis un Bot, je ne ressens pas la " \
               "douleur !\n https://git.gnous.eu/gnouseu/tuxbot-bot"
        em = discord.Embed(title='Repos TuxBot-Bot', description=text, colour=0xE9D460)
        em.set_author(name='Gnous', icon_url="https://cdn.discordapp.com/"
                                             "icons/280805240977227776/"
                                             "9ba1f756c9d9bfcf27989d0d0abb3862"
                                             ".png")
        await ctx.send(embed=em)

    """---------------------------------------------------------------------"""

    @commands.command(name='quote', pass_context=True)
    async def _quote(self, ctx, quote_id):
        global quoted_message

        async def get_message(message_id: int):
            for channel in ctx.message.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    test_chan = await self.bot.fetch_channel(channel.id)
                    try:
                        return await test_chan.fetch_message(message_id)
                    except (discord.NotFound, discord.Forbidden):
                        pass
            return None

        quoted_message = await get_message(int(quote_id))

        if quoted_message is not None:
            embed = discord.Embed(colour=quoted_message.author.colour,
                                  description=quoted_message.clean_content,
                                  timestamp=quoted_message.created_at)
            embed.set_author(name=quoted_message.author.display_name,
                             icon_url=quoted_message.author.avatar_url_as(
                                 format="jpg"))
            if len(quoted_message.attachments) >= 1:
                embed.set_image(url=quoted_message.attachments[0].url)
            embed.add_field(name="**Original**",
                            value=f"[Go!]({quoted_message.jump_url})")
            embed.set_footer(text="#" + quoted_message.channel.name)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Impossible de trouver le message.")


def setup(bot):
    bot.add_cog(Utility(bot))
