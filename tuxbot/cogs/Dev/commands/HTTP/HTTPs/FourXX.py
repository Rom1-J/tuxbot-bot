from .HttpCode import HttpCode


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
    "Http420",
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
    value = 400
    name = "Bad Request"
    mdn = True
    cat = True


class Http401(HttpCode):
    value = 401
    name = "Unauthorized"
    mdn = True
    cat = True


class Http402(HttpCode):
    value = 402
    name = "Payment Required"
    mdn = True
    cat = True


class Http403(HttpCode):
    value = 403
    name = "Forbidden"
    mdn = True
    cat = True


class Http404(HttpCode):
    value = 404
    name = "Not Found"
    mdn = True
    cat = True


class Http405(HttpCode):
    value = 405
    name = "Method Not Allowed"
    mdn = True
    cat = True


class Http406(HttpCode):
    value = 406
    name = "Not Acceptable"
    mdn = True
    cat = True


class Http407(HttpCode):
    value = 407
    name = "Proxy Authentication Required"
    mdn = True
    cat = False


class Http408(HttpCode):
    value = 408
    name = "Request Timeout"
    mdn = True
    cat = True


class Http409(HttpCode):
    value = 409
    name = "Conflict"
    mdn = True
    cat = True


class Http410(HttpCode):
    value = 410
    name = "Gone"
    mdn = True
    cat = True


class Http411(HttpCode):
    value = 411
    name = "Length Required"
    mdn = True
    cat = True


class Http412(HttpCode):
    value = 412
    name = "Precondition Failed"
    mdn = True
    cat = True


class Http413(HttpCode):
    value = 413
    name = "Payload Too Large"
    mdn = True
    cat = True


class Http414(HttpCode):
    value = 414
    name = "URI Too Long"
    mdn = True
    cat = True


class Http415(HttpCode):
    value = 415
    name = "Unsupported Media Type"
    mdn = True
    cat = True


class Http416(HttpCode):
    value = 416
    name = "Range Not Satisfiable"
    mdn = True
    cat = True


class Http417(HttpCode):
    value = 417
    name = "Expectation Failed"
    mdn = True
    cat = True


class Http418(HttpCode):
    value = 418
    name = "I'm a teapot"
    mdn = True
    cat = True


class Http420(HttpCode):
    value = 420
    name = "Enhanced Your Calm"
    mdn = False
    cat = True


class Http421(HttpCode):
    value = 421
    name = "Misdirected Request"
    mdn = False
    cat = True


class Http422(HttpCode):
    value = 422
    name = "Unprocessable Entity (WebDAV)"
    mdn = True
    cat = True


class Http423(HttpCode):
    value = 423
    name = "Locked (WebDAV)"
    mdn = False
    cat = True


class Http424(HttpCode):
    value = 424
    name = "Failed Dependency (WebDAV)"
    mdn = False
    cat = True


class Http425(HttpCode):
    value = 425
    name = "Too Early"
    mdn = True
    cat = True


class Http426(HttpCode):
    value = 426
    name = "Upgrade Required"
    mdn = True
    cat = True


class Http428(HttpCode):
    value = 428
    name = "Precondition Required"
    mdn = True
    cat = False


class Http429(HttpCode):
    value = 429
    name = "Too Many Requests"
    mdn = True
    cat = True


class Http431(HttpCode):
    value = 431
    name = "Request Header Fields Too Large"
    mdn = True
    cat = True


class Http451(HttpCode):
    value = 451
    name = "Unavailable For Legal Reasons"
    mdn = True
    cat = True
