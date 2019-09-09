import json


class Config:
    __slots__ = ('name', '_db')

    def __init__(self, name):
        self.name = name

        try:
            with open(self.name, 'r') as f:
                self._db = json.load(f)
        except FileNotFoundError:
            self._db = {}

    def __contains__(self, item):
        return item in self._db

    def __getitem__(self, item):
        return self._db[str(item)]

    def get(self, key, *args):
        """Retrieves a config entry."""
        return self._db.get(str(key), *args)

    def all(self) -> dict:
        return self._db
