from pip._internal import main as pip
import shutil

from .langs import locales, texts


class Config:
    def __init__(self):
        self.config = {
            'log_channel_id': '<INSERT_LOG_CHANNEL_HERE (in int)>',
            'main_server_id': '<INSERT_MAIN_CHANNEL_ID_HERE (in int)>',
            'authorized_id': '[admin ids here (in int)]',
        }

        with open('requirements.txt', 'r') as f:
            self.packages = f.read().split('\n')

    def input(self, key, **kwargs):
        locale = self.config.get('locale', 'multiple')

        print('\n\033[4m' + texts.get(locale).get(key) + '\033[0m')
        response = input('> ')

        if kwargs.get('valid'):
            while response not in kwargs.get('valid'):
                print('\033[36m' + '/'.join(kwargs.get('valid')) + '\033[0m')
                response = input('> ')

        if not kwargs.get('empty', True):
            while len(response) == 0:
                print('\033[41m' + texts.get(locale).get('not_empty')
                      + '\033[0m')
                response = input('> ')
        else:
            response = kwargs.get('default', None) if len(response) == 0 \
                else response

        self.config[key] = response

    def install(self):
        self.input('locale', valid=locales)
        print('\n\n\033[4;36m'
              + texts.get(self.config.get('locale')).get('install')
              + '\033[0m\n')

        for package in self.packages:
            pip(['install', package])

    def ask(self):
        print('\n\n\033[4;36m' + texts.get(self.config.get('locale'))
              .get('conf') + '\033[0m\n')

        self.input('token', empty=False)
        self.input('postgresql_username', empty=False)
        self.input('postgresql_password', empty=False)
        self.input('postgresql_dbname', empty=False)

        print('\n\n\033[4;36m' + texts.get(self.config.get('locale'))
              .get('logs') + '\033[0m\n')

        self.input('wh_id', empty=True)
        self.input('wh_token', empty=True)

        print('\n\n\033[4;36m' + texts.get(self.config.get('locale'))
              .get('misc') + '\033[0m\n')

        self.input('activity', empty=True)

    def save(self):
        with open('config.py', 'w') as file:
            postgresql = f"postgresql://" \
                         f"{self.config.get('postgresql_username')}:" \
                         f"{self.config.get('postgresql_password')}" \
                         f"@localhost/{self.config.get('postgresql_dbname')}"
            file.write(f"postgresql = '{postgresql}'\n")

            logs_webhook = dict(id=int(self.config.get('wh_id')),
                                token=self.config.get('wh_token'))
            file.write(f"logs_webhook = '{logs_webhook}'\n")

            for key, value in self.config.items():
                if not key.startswith('postgresql_') \
                        and not key.startswith('wh_'):
                    value = f"'{value}'" if type(value) is str else value
                    file.write(f"{key} = {value}\n")
        print('\n\n\033[4;36m' + texts.get(self.config.get('locale'))
              .get('end') + '\033[0m\n')

    def clean(self):
        print('\n\n\033[4;36m'
              + texts.get(self.config.get('locale')).get('clean')
              + '\033[0m\n')
        shutil.rmtree('first_run')
