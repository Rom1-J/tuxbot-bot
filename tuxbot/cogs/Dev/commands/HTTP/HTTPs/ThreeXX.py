from .HttpCode import HttpCode


__all__ = (
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
    value = 300
    name = "Multiple Choices"
    mdn = True
    cat = True


class Http301(HttpCode):
    value = 301
    name = "Moved Permanently"
    mdn = True
    cat = True


class Http302(HttpCode):
    value = 302
    name = "Found"
    mdn = True
    cat = True


class Http303(HttpCode):
    value = 303
    name = "See Other"
    mdn = True
    cat = True


class Http304(HttpCode):
    value = 304
    name = "Not Modified"
    mdn = True
    cat = True


class Http305(HttpCode):
    value = 305
    name = "Use Proxy"
    mdn = False
    cat = True


class Http306(HttpCode):
    value = 306
    name = "Unused"
    mdn = False
    cat = False


class Http307(HttpCode):
    value = 307
    name = "Temporary Redirect"
    mdn = True
    cat = True


class Http308(HttpCode):
    value = 308
    name = "Permanent Redirect"
    mdn = True
    cat = True
