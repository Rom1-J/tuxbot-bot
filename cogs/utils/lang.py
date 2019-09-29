import gettext
import config


class Texts:
    def __init__(self, base: str = 'base'):
        self.locale = config.locale
        self.base = base

    def get(self, text: str) -> str:
        texts = gettext.translation(self.base, localedir='extras/locales',
                                    languages=[self.locale])
        texts.install()
        return texts.gettext(text)

    def set(self, lang: str):
        self.locale = lang
