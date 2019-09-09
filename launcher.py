import asyncio
import contextlib
import logging
import socket
import sys

import click

from bot import TuxBot
from cogs.utils.db import Table

try:
    import config
    from cogs.utils.lang import gettext
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


def run_bot(unload):
    loop = asyncio.get_event_loop()
    log = logging.getLogger()

    try:
        pool = loop.run_until_complete(
            Table.create_pool(config.postgresql, command_timeout=60)
        )
    except socket.gaierror as e:
        click.echo(gettext('Could not set up PostgreSQL...'), file=sys.stderr)
        log.exception(gettext('Could not set up PostgreSQL...'))
        return

    bot = TuxBot(unload)
    bot.pool = pool
    bot.run()


@click.group(invoke_without_command=True, options_metavar='[options]')
@click.option('-u', '--unload',
              multiple=True, type=str,
              help=gettext('Launch without loading the <TEXT> module'))
@click.pass_context
def main(ctx, unload):
    if ctx.invoked_subcommand is None:
        with setup_logging():
            run_bot(unload)


if __name__ == '__main__':
    main()
