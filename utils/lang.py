import gettext
from .config import Config
from utils import Database

from .models.lang import LangModel
from discord.ext import commands


class Texts:
    def __init__(self, base: str = 'base', ctx: commands.Context = None):
        self.locale = self.get_locale(ctx)
        self.base = base

    def get(self, text: str) -> str:
        texts = gettext.translation(self.base, localedir='extras/locales',
                                    languages=[self.locale])
        texts.install()
        return texts.gettext(text)

    def set(self, lang: str):
        self.locale = lang

    @staticmethod
    def get_locale(ctx):
        database = Database(Config("./configs/config.cfg"))

        if ctx is not None:
            current = database.session\
                .query(LangModel.value)\
                .filter(LangModel.key == str(ctx.guild.id))
            if current.count() > 0:
                return current.one()[0]

        default = database.session\
            .query(LangModel.value)\
            .filter(LangModel.key == 'default')\
            .one()[0]
        return default
