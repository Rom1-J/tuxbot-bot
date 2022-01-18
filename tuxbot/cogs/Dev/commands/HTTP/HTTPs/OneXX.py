from . import HttpCode

__all__ = ("Http100", "Http101", "Http102", "Http103")


class Http100(HttpCode):
    def __init__(self):
        super().__init__(value=100, name="Continue", mdn=True, cat=True)


class Http101(HttpCode):
    def __init__(self):
        super().__init__(
            value=101, name="Switching Protocol", mdn=True, cat=True
        )


class Http102(HttpCode):
    def __init__(self):
        super().__init__(
            value=102, name="Processing (WebDAV)", mdn=False, cat=True
        )


class Http103(HttpCode):
    def __init__(self):
        super().__init__(value=103, name="Early Hints", mdn=True, cat=False)
