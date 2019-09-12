import gettext
import config


class Texts:
    def __init__(self, base: str = 'base'):
        self.locale = config.locale
        self.texts = gettext.translation(base, localedir='locales',
                                         languages=[self.locale])
        self.texts.install()

    def __str__(self) -> str:
        return self.texts

    def get(self, text: str) -> str:
        return self.texts.gettext(text)
