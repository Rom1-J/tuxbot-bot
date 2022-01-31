from . import HttpCode

_all__ = (
    "Http300",
    "Http301",
    "Http302",
    "Http303",
    "Http304",
    "Http305",
    "Http306",
    "Http307",
    "Http308",
)


class Http300(HttpCode):
    def __init__(self):
        super().__init__(
            value=300, name="Multiple Choices", mdn=True, cat=True
        )


class Http301(HttpCode):
    def __init__(self):
        super().__init__(
            value=301, name="Moved Permanently", mdn=True, cat=True
        )


class Http302(HttpCode):
    def __init__(self):
        super().__init__(value=302, name="Found", mdn=True, cat=True)


class Http303(HttpCode):
    def __init__(self):
        super().__init__(value=303, name="See Other", mdn=True, cat=True)


class Http304(HttpCode):
    def __init__(self):
        super().__init__(value=304, name="Not Modified", mdn=True, cat=True)


class Http305(HttpCode):
    def __init__(self):
        super().__init__(value=305, name="Use Proxy", mdn=False, cat=True)


class Http306(HttpCode):
    def __init__(self):
        super().__init__(value=306, name="Unused", mdn=False, cat=False)


class Http307(HttpCode):
    def __init__(self):
        super().__init__(
            value=307, name="Temporary Redirect", mdn=True, cat=True
        )


class Http308(HttpCode):
    def __init__(self):
        super().__init__(
            value=308, name="Permanent Redirect", mdn=True, cat=True
        )
