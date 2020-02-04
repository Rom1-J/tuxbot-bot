import gettext
import json

from discord.ext import commands


class Texts:
    def __init__(self, base: str = 'base', ctx: commands.Context = None):
        self.locale = self.get_locale(ctx)
        self.base = base

    def get(self, text: str) -> str:
        texts = gettext.translation(self.base, localedir='utils/locales',
                                    languages=[self.locale])
        texts.install()
        return texts.gettext(text)

    def set(self, lang: str):
        self.locale = lang

    @staticmethod
    def get_locale(ctx: commands.Context):
        lang = 'fr'
        if ctx is not None:
            try:
                with open(f'./configs/guilds/{ctx.guild.id}.json', 'r') as f:
                    data = json.load(f)

                lang = data['lang']

            except FileNotFoundError:
                pass

        return lang
