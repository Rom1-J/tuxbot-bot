from discord.ext import commands
import discord
import random
import json
import datetime, pytz
import calendar

import requests
import urllib


class Utility:
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
			

	"""--------------------------------------------------------------------------------------------------------------------------"""

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

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command(name='hastebin', pass_context=True)
	async def _hastebin(self, ctx, *, data):
		"""Poster sur Hastebin."""
		await ctx.message.delete()

		post = requests.post("https://hastebin.com/documents", data=data)

		try:
			await ctx.send(f"{ctx.message.author.mention} message posté avec succès sur :\nhttps://hastebin.com/{post.json()['key']}.txt")
		except json.JSONDecodeError:
			await ctx.send("Impossible de poster ce message. L'API doit être HS.")

	"""---------------------------------------------------------------------"""

	@commands.command(name='iplocalise', pass_context=True)
	async def _iplocalise(self, ctx, ipaddress):
		"""Recup headers."""
		if ipaddress.startswith("http://"):
			ipaddress = ipaddress.split("http://")[1]
		if ipaddress.startswith("https://"):
			ipaddress = ipaddress.split("https://")[1]
		iploading = await ctx.send("_réfléchis..._")
		ipapi = urllib.request.urlopen("http://ip-api.com/json/" + ipaddress)
		ipinfo = json.loads(ipapi.read().decode())

		if ipinfo["status"] != "fail":
			await iploading.edit(content="L'adresse IP ``{query}`` appartient à ``{org}`` et se situe à ``{city}``, dans ``{regionName}``, ``{country}``.".format(**ipinfo))
		else:
			await iploading.edit(content=f"Erreur, impossible d'avoir des informations sur l'adresse IP {ipinfo['query']}")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	@commands.command(name='getheaders', pass_context=True)
	async def _getheaders(self, ctx, *, adresse):
		"""Recuperer les HEADERS :d"""
		print("Loaded")
		if adresse.startswith("http://") != True and adresse.startswith("https://") != True:
			 adresse = "http://" + adresse
		if len(adresse) > 200:
			await ctx.send("{0} Essaye d'entrer une adresse de moins de 200 caractères plutôt.".format(ctx.author.mention))
		elif adresse.startswith("http://") or adresse.startswith("https://") or adresse.startswith("ftp://"):
			try:
				get = urllib.request.urlopen(adresse, timeout = 1)
				embed = discord.Embed(title="Entêtes de {0}".format(adresse), color=0xd75858)
				embed.add_field(name="Code Réponse", value=get.getcode(), inline = True)
				embed.set_thumbnail(url="https://http.cat/{}".format(str(get.getcode())))
				if get.getheader('location'):
					embed.add_field(name="Redirection vers", value=get.getheader('location'), inline=True)
				if get.getheader('server'):
					embed.add_field(name="Serveur", value=get.getheader('server'), inline=True)
				if get.getheader('content-type'):
					embed.add_field(name="Type de contenu", value = get.getheader('content-type'), inline = True)
				if get.getheader('x-content-type-options'):
					embed.add_field(name="x-content-type", value= get.getheader('x-content-type-options'), inline=True)
				if get.getheader('x-frame-options'):
					embed.add_field(name="x-frame-options", value= get.getheader('x-frame-options'), inline=True)
				if get.getheader('cache-control'):
					embed.add_field(name="Controle du cache", value = get.getheader('cache-control'), inline = True)
				await ctx.send(embed=embed)
			except urllib.error.HTTPError as e:
				embed = discord.Embed(title="Entêtes de {0}".format(adresse), color=0xd75858)
				embed.add_field(name="Code Réponse", value=e.getcode(), inline = True)
				embed.set_thumbnail(url="https://http.cat/{}".format(str(e.getcode())))
				await ctx.send(embed=embed)
				print('''An error occurred: {} The response code was {}'''.format(e, e.getcode()))
			except urllib.error.URLError as e:
				print("ERROR @ getheaders @ urlerror : {} - adress {}".format(e, adresse))
				await ctx.send('[CONTACTER ADMIN] URLError: {}'.format(e.reason))
			except Exception as e:
				print("ERROR @ getheaders @ Exception : {} - adress {}".format(e, adresse))
				await ctx.send("{0} Impossible d'accèder à {1}, es-tu sur que l'adresse {1} est correcte et que le serveur est allumé ?".format(ctx.author.mention, adresse))
		else:
			await ctx.send("{0} Merci de faire commencer {1} par ``https://``, ``http://`` ou ``ftp://``.".format(ctx.message.author.mention, adresse))
	
	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@commands.command(name='github', pass_context=True)
	async def _github(ctx):
		"""Pour voir mon code"""
		text = "How tu veux voir mon repos Github pour me disséquer ? Pas de soucis ! Je suis un Bot, je ne ressens pas la douleur !\n https://github.com/outout14/tuxbot-bot"
		em = discord.Embed(title='Repos TuxBot-Bot', description=text, colour=0xE9D460)
		em.set_author(name='Outout', icon_url="https://avatars0.githubusercontent.com/u/14958554?v=3&s=400")
		await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Utility(bot))
