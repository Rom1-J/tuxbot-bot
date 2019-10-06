try:
    import config
    from cogs.utils.lang import Texts
except ModuleNotFoundError:
    import extras.first_run

import contextlib
import logging
import socket
import sys

import click
import git
import requests

from bot import TuxBot
from cogs.utils.database import Database


@contextlib.contextmanager
def setup_logging():
    try:
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)

        handler = logging.FileHandler(filename='logs/tuxbot.log',
                                      encoding='utf-8', mode='w')
        fmt = logging.Formatter('[{levelname:<7}] [{asctime}]'
                                ' {name}: {message}',
                                '%Y-%m-%d %H:%M:%S', style='{')

        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)


def run_bot(unload: list = []):
    log = logging.getLogger()

    print(Texts().get('Starting...'))

    try:
        database = Database(config)
    except socket.gaierror:
        click.echo(Texts().get("Could not set up PostgreSQL..."),
                   file=sys.stderr)
        log.exception(Texts().get("Could not set up PostgreSQL..."))
        return

    bot = TuxBot(unload, database)
    bot.run()


@click.command()
@click.option('-d', '--unload', multiple=True, type=str,
              help=Texts().get("Launch without loading the <TEXT> module"))
@click.option('-u', '--update', is_flag=True,
              help=Texts().get("Search for update"))
def main(**kwargs):
    if kwargs.get('update'):
        _update()

    with setup_logging():
        run_bot(kwargs.get('unload'))


@click.option('-d', '--update', is_flag=True,
              help=Texts().get("Search for update"))
def _update():
    print(Texts().get("Checking for update..."))

    local = git.Repo(search_parent_directories=True)
    current = local.head.object.hexsha

    gitea = 'https://git.gnous.eu/api/v1/'
    origin = requests.get(gitea + 'repos/gnouseu/tuxbot-bot/branches/rewrite')
    last = origin.json().get('commit').get('id')

    if current != last:
        print(Texts().get("A new version is available !"))
        check = None

        while check not in ['', 'y', 'n', 'o']:
            check = input(Texts().get("Update ? [Y/n] ")).lower().strip()
            print(check)

            if check in ['y', '', 'o']:
                print(Texts().get("Downloading..."))

                origin = git.Repo(search_parent_directories=True) \
                    .remotes['origin']
                origin.pull()

                with setup_logging():
                    run_bot()
            else:
                with setup_logging():
                    run_bot()
    else:
        print(Texts().get("Tuxbot is up to date") + '\n')

        with setup_logging():
            run_bot()


if __name__ == '__main__':
    main()
