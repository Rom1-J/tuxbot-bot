import gettext
import config

lang = gettext.translation('base', localedir='locales',
                           languages=[config.lang])
lang.install()

_ = lang.gettext
