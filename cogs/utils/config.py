import configparser


class Config:
    __slots__ = ('name', '_db')

    def __init__(self, name):
        self.name = name

        self._db: configparser.ConfigParser = configparser.ConfigParser()
        self._db.read(self.name)

    def __contains__(self, item):
        return item in self._db

    def __getitem__(self, item):
        return self._db[item]

    def all(self) -> list:
        return self._db.sections()

    def get(self, *args, **kwargs) -> str:
        return self._db.get(*args, **kwargs)
