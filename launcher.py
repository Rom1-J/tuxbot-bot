import logging
import contextlib


try:
    import config
except ModuleNotFoundError:
    import first_run


@contextlib.contextmanager
def setup_logging():
    try:
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)

        handler = logging.FileHandler(filename='logs/tuxbot.log',
                                      encoding='utf-8', mode='w')
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}]'
                                ' {name}: {message}',
                                '%Y-%m-%d %H:%M:%S', style='{')

        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


def run_bot():
    pass  # Todo: initialize bot, postgresql,...


if __name__ == '__main__':
    with setup_logging():
        run_bot()
