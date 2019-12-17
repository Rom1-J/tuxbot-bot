import configparser


class Config(configparser.RawConfigParser):
    __slots__ = ('name', '_db')

    def __init__(self, name):
        super().__init__()
        self.name = name

        self._db = super()
        self._db.read(self.name)

    def all(self) -> list:
        return self._db.sections()
