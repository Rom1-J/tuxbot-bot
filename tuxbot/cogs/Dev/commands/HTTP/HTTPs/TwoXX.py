from . import HttpCode

__all__ = (
    "Http200",
    "Http201",
    "Http202",
    "Http203",
    "Http204",
    "Http205",
    "Http206",
    "Http207",
    "Http208",
    "Http226",
)


class Http200(HttpCode):
    def __init__(self):
        super().__init__(value=200, name="OK", mdn=True, cat=True)


class Http201(HttpCode):
    def __init__(self):
        super().__init__(value=201, name="Created", mdn=True, cat=True)


class Http202(HttpCode):
    def __init__(self):
        super().__init__(value=202, name="Accepted", mdn=True, cat=True)


class Http203(HttpCode):
    def __init__(self):
        super().__init__(
            value=203,
            name="Non-Authoritative Information",
            mdn=True,
            cat=False,
        )


class Http204(HttpCode):
    def __init__(self):
        super().__init__(value=204, name="No Content", mdn=True, cat=True)


class Http205(HttpCode):
    def __init__(self):
        super().__init__(value=205, name="Reset Content", mdn=True, cat=False)


class Http206(HttpCode):
    def __init__(self):
        super().__init__(value=206, name="Partial Content", mdn=True, cat=True)


class Http207(HttpCode):
    def __init__(self):
        super().__init__(
            value=207, name="Multi-Status (WebDAV)", mdn=False, cat=True
        )


class Http208(HttpCode):
    def __init__(self):
        super().__init__(
            value=208, name="Already Reported (WebDAV)", mdn=False, cat=False
        )


class Http226(HttpCode):
    def __init__(self):
        super().__init__(
            value=226,
            name="IM Used (HTTP Delta encoding)",
            mdn=False,
            cat=False,
        )
