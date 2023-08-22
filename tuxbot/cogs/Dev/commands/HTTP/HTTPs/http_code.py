import typing


class HttpCode(typing.TypedDict):
    value: int
    name: str
    mdn: bool
    cat: bool
