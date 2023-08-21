import typing


class HttpCode:
    _value: int
    _name: str
    _mdn: bool
    _cat: bool

    # =========================================================================
    # =========================================================================

    @property
    def value(self: typing.Self) -> int:
        return self._value

    @value.setter
    def value(self: typing.Self, val: int) -> None:
        if not isinstance(val, int):
            raise TypeError

        self._value = val

    # =========================================================================

    @property
    def name(self: typing.Self) -> str:
        return self._name

    @name.setter
    def name(self: typing.Self, val: str) -> None:
        if not isinstance(val, str):
            raise TypeError

        self._name = val

    # =========================================================================

    @property
    def mdn(self: typing.Self) -> bool:
        return self._mdn

    @mdn.setter
    def mdn(self: typing.Self, val: bool) -> None:
        if not isinstance(val, bool):
            raise TypeError

        self._mdn = val

    # =========================================================================

    @property
    def cat(self: typing.Self) -> bool:
        return self._cat

    @cat.setter
    def cat(self: typing.Self, val: bool) -> None:
        if not isinstance(val, bool):
            raise TypeError

        self._cat = val

    # =========================================================================
