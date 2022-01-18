class HttpCode:
    def __init__(self, value: int, name: str, mdn: bool, cat: bool):
        self.value = value
        self.name = name
        self.mdn = mdn
        self.cat = cat

    # =========================================================================
    # =========================================================================

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, int):
            raise TypeError

        self._value = val

    # =========================================================================

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError

        self._name = val

    # =========================================================================

    @property
    def mdn(self):
        return self._mdn

    @mdn.setter
    def mdn(self, val):
        if not isinstance(val, bool):
            raise TypeError

        self._mdn = val

    # =========================================================================

    @property
    def cat(self):
        return self._cat

    @cat.setter
    def cat(self, val):
        if not isinstance(val, bool):
            raise TypeError

        self._cat = val

    # =========================================================================
