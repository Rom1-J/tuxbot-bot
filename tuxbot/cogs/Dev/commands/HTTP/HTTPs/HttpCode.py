class HttpCode:
    _value: int
    _name: str
    _mdn: bool
    _cat: bool

    # =========================================================================
    # =========================================================================

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int) -> None:
        if not isinstance(val, int):
            raise TypeError

        self._value = val

    # =========================================================================

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        if not isinstance(val, str):
            raise TypeError

        self._name = val

    # =========================================================================

    @property
    def mdn(self) -> bool:
        return self._mdn

    @mdn.setter
    def mdn(self, val: bool) -> None:
        if not isinstance(val, bool):
            raise TypeError

        self._mdn = val

    # =========================================================================

    @property
    def cat(self) -> bool:
        return self._cat

    @cat.setter
    def cat(self, val: bool) -> None:
        if not isinstance(val, bool):
            raise TypeError

        self._cat = val

    # =========================================================================
