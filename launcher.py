import asyncio
import contextlib
import logging
import socket
import sys
import git
import requests

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


def run_bot(unload: list = []):
    loop = asyncio.get_event_loop()
    log = logging.getLogger()

    print(gettext('Stating...'))

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


@click.command()
@click.option('-d', '--unload', multiple=True, type=str, help=gettext('Launch without loading the <TEXT> module'))
@click.option('-u', '--update', help=gettext('Search for update'), is_flag=True)
def main(**kwargs):
    if kwargs.get('update'):
        _update()

    with setup_logging():
        run_bot(kwargs.get('unload'))


@click.option('-d', '--update', help=gettext('Search for update'), is_flag=True)
def _update():
    print(gettext('Checking for update...'))

    local = git.Repo(search_parent_directories=True)
    current = local.head.object.hexsha

    origin = requests.get('https://git.gnous.eu/api/v1/repos/gnouseu/tuxbot-bot/branches/master')
    last = origin.json().get('commit').get('id')

    if current != last:
        print(gettext('A new version is available !'))
        check = None

        while check not in ['', 'y', 'n', 'o']:
            check = input(gettext('Update ? [Y/n] ')).lower().strip()
            print(check)

            if check in ['y', '', 'o']:
                print(gettext('Downloading...'))

                origin = git.Repo(search_parent_directories=True).remotes['origin']
                origin.pull()

                with setup_logging():
                    run_bot()
            else:
                with setup_logging():
                    run_bot()
    else:
        print(gettext('Tuxbot is up to date') + '\n')

        with setup_logging():
            run_bot()


if __name__ == '__main__':
    main()
