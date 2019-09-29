import gettext
import config

from .models.lang import Lang
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
        engine = create_engine(config.postgresql)

        Session = sessionmaker()
        Session.configure(bind=engine)

        session = Session()

        if ctx is not None:
            current = session\
                .query(Lang.value)\
                .filter(Lang.key == str(ctx.guild.id))
            if current.count() > 0:
                return current.one()[0]

        default = session\
            .query(Lang.value)\
            .filter(Lang.key == 'default')\
            .one()[0]
        return default
