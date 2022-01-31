from . import HttpCode

__all__ = (
    "Http500",
    "Http501",
    "Http502",
    "Http503",
    "Http504",
    "Http505",
    "Http506",
    "Http507",
    "Http508",
    "Http509",
    "Http510",
    "Http511",
)


class Http500(HttpCode):
    def __init__(self):
        super().__init__(
            value=500, name="Internal Server Error", mdn=True, cat=True
        )


class Http501(HttpCode):
    def __init__(self):
        super().__init__(value=501, name="Not Implemented", mdn=True, cat=True)


class Http502(HttpCode):
    def __init__(self):
        super().__init__(value=502, name="Bad Gateway", mdn=True, cat=True)


class Http503(HttpCode):
    def __init__(self):
        super().__init__(
            value=503, name="Service Unavailable", mdn=True, cat=True
        )


class Http504(HttpCode):
    def __init__(self):
        super().__init__(value=504, name="Gateway Timeout", mdn=True, cat=True)


class Http505(HttpCode):
    def __init__(self):
        super().__init__(
            value=505, name="HTTP Version Not Supported", mdn=True, cat=False
        )


class Http506(HttpCode):
    def __init__(self):
        super().__init__(
            value=506, name="Variant Also Negotiates", mdn=True, cat=True
        )


class Http507(HttpCode):
    def __init__(self):
        super().__init__(
            value=507, name="Insufficient Storage (WebDAV)", mdn=True, cat=True
        )


class Http508(HttpCode):
    def __init__(self):
        super().__init__(
            value=508, name="Loop Detected (WebDAV)", mdn=True, cat=True
        )


class Http509(HttpCode):
    def __init__(self):
        super().__init__(
            value=509, name="Bandwidth Limit Exceeded", mdn=False, cat=True
        )


class Http510(HttpCode):
    def __init__(self):
        super().__init__(value=510, name="Not Extended", mdn=True, cat=True)


class Http511(HttpCode):
    def __init__(self):
        super().__init__(
            value=511,
            name="Network Authentication Required",
            mdn=True,
            cat=True,
        )
