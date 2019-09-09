import gettext
import config

lang = gettext.translation('base', localedir='locales',
                           languages=[config.lang])
lang.install()

gettext = lang.gettext
