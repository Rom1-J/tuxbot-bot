from .langs import locales, texts


class Config:
    def __init__(self):
        self.config = {
            'log_channel_id': '<INSERT_LOG_CHANNEL_HERE (in int)>',
            'main_server_id': '<INSERT_MAIN_CHANNEL_ID_HERE (in int)>',
            'authorized_id': '[admin ids here (in int)]',
            'unkickable_id': '[unkickable ids here (in int)]'
        }

    def input(self, key, **kwargs):
        lang = self.config.get('lang', 'multiple')

        print('\n\033[4m' + texts.get(lang).get(key) + '\033[0m')
        response = input('> ')

        if kwargs.get('valid'):
            while response not in kwargs.get('valid'):
                print('\033[36m' + '/'.join(kwargs.get('valid')) + '\033[0m')
                response = input('> ')

        if not kwargs.get('empty', True):
            while len(response) == 0:
                print('\033[41m' + texts.get(lang).get('not_empty')
                      + '\033[0m')
                response = input('> ')
        else:
            response = kwargs.get('default', None) if len(response) == 0 \
                else response

        self.config[key] = response

    def ask(self):
        self.input('lang', valid=locales)
        self.input('token', empty=False)
        self.input('postgresql_username', empty=False)
        self.input('postgresql_password', empty=False)
        self.input('postgresql_dbname', empty=False)

        print('\n\n\033[4;36m' + texts.get(self.config.get('lang')).get('misc')
              + '\033[0m\n')

        self.input('activity', empty=True)
        self.input('prefix', empty=True)

    def save(self):
        with open('config.py', 'w') as file:
            postgresql = f"postgresql://" \
                         f"{self.config.get('postgresql_username')}:" \
                         f"{self.config.get('postgresql_password')}@host/" \
                         f"{self.config.get('postgresql_dbname')}"
            file.write(f"postgresql = '{postgresql}'\n")

            for key, value in self.config.items():
                if not key.startswith('postgresql_'):
                    value = f"'{value}'" if type(value) is str else value
                    file.write(f"{key} = {value}\n")
        print('\n\n\033[4;36m' + texts.get(self.config.get('lang')).get('end')
              + '\033[0m\n')
