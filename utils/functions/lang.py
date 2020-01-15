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
    def get_locale(ctx):
        with open('./configs/langs.json') as f:
            data = json.load(f)

        if ctx is not None:
            return data.get(str(ctx.guild.id), data['default'])
        else:
            return data['default']
