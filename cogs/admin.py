from discord.ext import commands
import discord
import aiohttp
import asyncio
import time
from .utils import checks

from .utils.checks import get_user

import json
import random

import datetime

import requests


class Admin:
	"""Commandes secrètes d'administration."""


	def __init__(self, bot):
		self.bot = bot

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(pass_context=True)
	async def ban(self, ctx, user, *, reason=""):
		"""Ban user"""
		user = get_user(ctx.message, user)
		if user:
			try:
				await user.ban(reason=reason)
				return_msg = "`{}` a été banni\n".format(user.mention)
				if reason:
					return_msg += "raison : `{}`".format(reason)
				return_msg += "."
				await ctx.send(return_msg)
			except discord.Forbidden:
				await ctx.send('Impossible de bannir cet user, probleme de permission.')
		else:
			return await ctx.send('Impossible de trouver l\'user.')

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(pass_context=True)
	async def kick(self, ctx, user, *, reason=""):
		"""Kick a user"""
		user = get_user(ctx.message, user)
		if user:
			try:
				await user.kick(reason=reason)
				return_msg = "`{}` a été kické\n".format(user.mention)
				if reason:
					return_msg += "raison : `{}`".format(reason)
				return_msg += "."
				await ctx.send(return_msg)
			except discord.Forbidden:
				await ctx.send('Impossible de kicker cet user, probleme de permission.')
		else:
			return await ctx.send('Impossible de trouver l\'user.')

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='clear', pass_context=True)
	async def _clear(self, ctx, number: int, silent: str = True):
		"""Clear <number> of message(s)"""
		try:
			await ctx.message.delete()
		except:
			print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
		if number < 1000:
			async for message in ctx.message.channel.history(limit=number):
				try:
					await message.delete()
				except Exception as e: #TODO : A virer dans l'event on_error
					if silent is not True:
						await ctx.send(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))
			if silent is not True:
				await ctx.send("Hop voila j'ai viré des messages! Hello World")
			print(str(number)+" messages ont été supprimés")
		else:
			await ctx.send('Trop de messages, entre un nombre < 1000')

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='say', pass_context=True)
	async def _say(self, ctx, *, tosay:str):
		"""Say a message in the current channel"""
		try:
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			await ctx.send(tosay)
		except Exception as e: #TODO : A virer dans l'event on_error
			await ctx.send(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='sayto', pass_context=True)
	async def _sayto(self, ctx, id:int, *, tosay:str):
		"""Say a message in the <id> channel"""
		try:
			chan = self.bot.get_channel(id)
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			try:
				await chan.send(tosay)
			except Exception as e:
				print("Impossible d'envoyer le message dans " + str(id))
		except Exception as e: #TODO : A virer dans l'event on_error
			await ctx.send(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='sayto_dm', pass_context=True)
	async def _sayto_dm(self, ctx, id:int, *, tosay:str):
		"""Say a message to the <id> user"""
		try:
			user = self.bot.get_user(id)
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			try:
				await user.send(tosay)
			except Exception as e:
				print("Impossible d'envoyer le message dans " + str(id))
		except Exception as e: #TODO : A virer dans l'event on_error
			await ctx.send(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='editsay', pass_context=True)
	async def _editsay(self, ctx, id:int, *, new_content:str):
		"""Edit a bot's message"""
		try:
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			toedit = await ctx.channel.get_message(id)
		except discord.errors.NotFound:
			await ctx.send("Impossible de trouver le message avec l'id `{}` sur ce salon".format(id))
			return
		try:
			await toedit.edit(content=str(new_content))
		except discord.errors.Forbidden:
			await ctx.send("J'ai po les perms pour editer mes messages :(")

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='addreaction', pass_context=True)
	async def _addreaction(self, ctx, id:int, reaction:str):
		"""Add reactions to a message"""
		try:
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			toadd = await ctx.channel.get_message(id)
		except discord.errors.NotFound:
			await ctx.send("Impossible de trouver le message avec l'id `{}` sur ce salon".format(id))
			return
		try:
			await toadd.add_reaction(reaction)
		except discord.errors.Forbidden:
			await ctx.send("J'ai po les perms pour ajouter des réactions :(")

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='delete', pass_context=True)
	async def _delete(self, ctx, id:int):
		"""Delete message in current channel"""
		try:
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			todelete = await ctx.channel.get_message(id)
		except discord.errors.NotFound:
			await ctx.send("Impossible de trouver le message avec l'id `{}` sur ce salon".format(id))
			return
		try:
			await todelete.delete()
		except discord.errors.Forbidden:
			await ctx.send("J'ai po les perms pour supprimer des messages :(")

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='deletefrom', pass_context=True)
	async def _deletefrom(self, ctx, chan_id:int, *, message_id:str):
		"""Delete message in <chan_id> channel"""
		try:
			chan = self.bot.get_channel(chan_id)
			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			todelete = await chan.get_message(message_id)
		except discord.errors.NotFound:
			await ctx.send("Impossible de trouver le message avec l'id `{}` sur le salon".format(id))
			return
		try:
			await todelete.delete()
		except discord.errors.Forbidden:
			await ctx.send("J'ai po les perms pour supprimer le message :(")

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@checks.has_permissions(administrator=True)
	@commands.command(name='embed', pass_context=True)
	async def _embed(self, ctx, *, msg: str = "help"):
		"""Send an embed"""
		if msg != "help":
			ptext = title = description = image = thumbnail = color = footer = author = None
			timestamp = discord.Embed.Empty
			embed_values = msg.split('|')
			for i in embed_values:
				if i.strip().lower().startswith('ptext='):
					ptext = i.strip()[6:].strip()
				elif i.strip().lower().startswith('title='):
					title = i.strip()[6:].strip()
				elif i.strip().lower().startswith('description='):
					description = i.strip()[12:].strip()
				elif i.strip().lower().startswith('desc='):
					description = i.strip()[5:].strip()
				elif i.strip().lower().startswith('image='):
					image = i.strip()[6:].strip()
				elif i.strip().lower().startswith('thumbnail='):
					thumbnail = i.strip()[10:].strip()
				elif i.strip().lower().startswith('colour='):
					color = i.strip()[7:].strip()
				elif i.strip().lower().startswith('color='):
					color = i.strip()[6:].strip()
				elif i.strip().lower().startswith('footer='):
					footer = i.strip()[7:].strip()
				elif i.strip().lower().startswith('author='):
					author = i.strip()[7:].strip()
				elif i.strip().lower().startswith('timestamp'):
					timestamp = ctx.message.created_at
				else:
					if description is None and not i.strip().lower().startswith('field='):
						description = i.strip()

			if color:
				if color.startswith('#'):
					color = color[1:]
				if not color.startswith('0x'):
					color = '0x' + color

			if ptext is title is description is image is thumbnail is color is footer is author is None and 'field=' not in msg:
				try:
					await ctx.message.delete()
				except:
					print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
				return await ctx.send(content=None,
												   embed=discord.Embed(description=msg))

			if color:
				em = discord.Embed(timestamp=timestamp, title=title, description=description, color=int(color, 16))
			else:
				em = discord.Embed(timestamp=timestamp, title=title, description=description)
			for i in embed_values:
				if i.strip().lower().startswith('field='):
					field_inline = True
					field = i.strip().lstrip('field=')
					field_name, field_value = field.split('value=')
					if 'inline=' in field_value:
						field_value, field_inline = field_value.split('inline=')
						if 'false' in field_inline.lower() or 'no' in field_inline.lower():
							field_inline = False
					field_name = field_name.strip().lstrip('name=')
					em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
			if author:
				if 'icon=' in author:
					text, icon = author.split('icon=')
					if 'url=' in icon:
						em.set_author(name=text.strip()[5:], icon_url=icon.split('url=')[0].strip(), url=icon.split('url=')[1].strip())
					else:
						em.set_author(name=text.strip()[5:], icon_url=icon)
				else:
					if 'url=' in author:
						em.set_author(name=author.split('url=')[0].strip()[5:], url=author.split('url=')[1].strip())
					else:
						em.set_author(name=author)

			if image:
				em.set_image(url=image)
			if thumbnail:
				em.set_thumbnail(url=thumbnail)
			if footer:
				if 'icon=' in footer:
					text, icon = footer.split('icon=')
					em.set_footer(text=text.strip()[5:], icon_url=icon)
				else:
					em.set_footer(text=footer)

			try:
				await ctx.message.delete()
			except:
				print("Impossible de supprimer le message \"" + str(ctx.message.content) + "\"")
			await ctx.send(content=ptext, embed=em)

		else:
			embed=discord.Embed(title="Aide sur l'utilisation de la commande .embed:")
			embed.add_field(name="Titre:", value="title=<le titre>", inline=True)
			embed.add_field(name="Description:", value="description=<la description>", inline=True)
			embed.add_field(name="Couleur:", value="color=<couleur en hexa>", inline=True)
			embed.add_field(name="Image:", value="image=<url de l'image (en https)>", inline=True)
			embed.add_field(name="Thumbnail:", value="thumbnail=<url de l'image>", inline=True)
			embed.add_field(name="Auteur:", value="author=<nom de l'auteur>", inline=True)
			embed.add_field(name="Icon", value="icon=<url de l'image>", inline=True)
			embed.add_field(name="Footer", value="footer=<le footer>", inline=True)
			embed.set_footer(text="Exemple: .embed title=Un titre | description=Une description | color=3AB35E | field=name=test value=test")

			await ctx.send(embed=embed)

	"""--------------------------------------------------------------------------------------------------------------------------"""


def setup(bot):
	bot.add_cog(Admin(bot))
