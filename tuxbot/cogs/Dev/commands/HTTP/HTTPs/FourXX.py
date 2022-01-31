from . import HttpCode

__all__ = (
    "Http400",
    "Http401",
    "Http402",
    "Http403",
    "Http404",
    "Http405",
    "Http406",
    "Http407",
    "Http408",
    "Http409",
    "Http410",
    "Http411",
    "Http412",
    "Http413",
    "Http414",
    "Http415",
    "Http416",
    "Http417",
    "Http418",
    "Http421",
    "Http422",
    "Http423",
    "Http424",
    "Http425",
    "Http426",
    "Http428",
    "Http429",
    "Http431",
    "Http451",
)


class Http400(HttpCode):
    def __init__(self):
        super().__init__(value=400, name="Bad Request", mdn=True, cat=True)


class Http401(HttpCode):
    def __init__(self):
        super().__init__(value=401, name="Unauthorized", mdn=True, cat=True)


class Http402(HttpCode):
    def __init__(self):
        super().__init__(
            value=402, name="Payment Required", mdn=True, cat=True
        )


class Http403(HttpCode):
    def __init__(self):
        super().__init__(value=403, name="Forbidden", mdn=True, cat=True)


class Http404(HttpCode):
    def __init__(self):
        super().__init__(value=404, name="Not Found", mdn=True, cat=True)


class Http405(HttpCode):
    def __init__(self):
        super().__init__(
            value=405, name="Method Not Allowed", mdn=True, cat=True
        )


class Http406(HttpCode):
    def __init__(self):
        super().__init__(value=406, name="Not Acceptable", mdn=True, cat=True)


class Http407(HttpCode):
    def __init__(self):
        super().__init__(
            value=407,
            name="Proxy Authentication Required",
            mdn=True,
            cat=False,
        )


class Http408(HttpCode):
    def __init__(self):
        super().__init__(value=408, name="Request Timeout", mdn=True, cat=True)


class Http409(HttpCode):
    def __init__(self):
        super().__init__(value=409, name="Conflict", mdn=True, cat=True)


class Http410(HttpCode):
    def __init__(self):
        super().__init__(value=410, name="Gone", mdn=True, cat=True)


class Http411(HttpCode):
    def __init__(self):
        super().__init__(value=411, name="Length Required", mdn=True, cat=True)


class Http412(HttpCode):
    def __init__(self):
        super().__init__(
            value=412, name="Precondition Failed", mdn=True, cat=True
        )


class Http413(HttpCode):
    def __init__(self):
        super().__init__(
            value=413, name="Payload Too Large", mdn=True, cat=True
        )


class Http414(HttpCode):
    def __init__(self):
        super().__init__(value=414, name="URI Too Long", mdn=True, cat=True)


class Http415(HttpCode):
    def __init__(self):
        super().__init__(
            value=415, name="Unsupported Media Type", mdn=True, cat=True
        )


class Http416(HttpCode):
    def __init__(self):
        super().__init__(
            value=416, name="Range Not Satisfiable", mdn=True, cat=True
        )


class Http417(HttpCode):
    def __init__(self):
        super().__init__(
            value=417, name="Expectation Failed", mdn=True, cat=True
        )


class Http418(HttpCode):
    def __init__(self):
        super().__init__(value=418, name="I'm a teapot", mdn=True, cat=True)


class Http421(HttpCode):
    def __init__(self):
        super().__init__(
            value=421, name="Misdirected Request", mdn=False, cat=True
        )


class Http422(HttpCode):
    def __init__(self):
        super().__init__(
            value=422, name="Unprocessable Entity (WebDAV)", mdn=True, cat=True
        )


class Http423(HttpCode):
    def __init__(self):
        super().__init__(
            value=423, name="Locked (WebDAV)", mdn=False, cat=True
        )


class Http424(HttpCode):
    def __init__(self):
        super().__init__(
            value=424, name="Failed Dependency (WebDAV)", mdn=False, cat=True
        )


class Http425(HttpCode):
    def __init__(self):
        super().__init__(value=425, name="Too Early", mdn=True, cat=True)


class Http426(HttpCode):
    def __init__(self):
        super().__init__(
            value=426, name="Upgrade Required", mdn=True, cat=True
        )


class Http428(HttpCode):
    def __init__(self):
        super().__init__(
            value=428, name="Precondition Required", mdn=True, cat=False
        )


class Http429(HttpCode):
    def __init__(self):
        super().__init__(
            value=429, name="Too Many Requests", mdn=True, cat=True
        )


class Http431(HttpCode):
    def __init__(self):
        super().__init__(
            value=431,
            name="Request Header Fields Too Large",
            mdn=True,
            cat=True,
        )


class Http451(HttpCode):
    def __init__(self):
        super().__init__(
            value=451, name="Unavailable For Legal Reasons", mdn=True, cat=True
        )
