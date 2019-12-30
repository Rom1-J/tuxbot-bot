from typing import List, Union

import configparser


class Config(configparser.ConfigParser):
    __slots__ = ('name', '_db')

    def __init__(self, name):
        super().__init__()

        self._db = super()
        self._db.read(name)

    def find(self, value: str, **kwargs) \
            -> Union[
                List[configparser.SectionProxy], configparser.SectionProxy
            ]:
        key = kwargs.get('key', None)
        first = kwargs.get('first', False)

        results = []

        for name, section in self._db.items():
            if key is None:
                for k in section.keys():
                    if section.get(k) == value:
                        results.append(section)
                    if first and len(results) == 1:
                        return results[0]
            else:
                if section.get(key) == value:
                    results.append(section)
                if first and len(results) == 1:
                    return results[0]
        return results
