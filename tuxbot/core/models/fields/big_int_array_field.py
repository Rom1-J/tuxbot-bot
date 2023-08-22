"""
Big Int Array field specifically for PostgreSQL.

This field can store list of bigint values.
"""
import json
import typing

from tortoise.fields import Field
from tortoise.models import Model


class _KwargsT(typing.TypedDict):
    _: typing.Any


class BigIntArrayField(Field[list[int]]):
    """
    Big Int Array field specifically for PostgreSQL.

    This field can store list of bigint values.
    """

    SQL_TYPE = "bigint[]"

    def __init__(self: typing.Self, **kwargs: typing.Unpack[_KwargsT]) -> None:
        super().__init__(**kwargs)

    def to_db_value(
        self: typing.Self,
        value: list[int],
        instance: type[Model] | Model,  # noqa: ARG002
    ) -> list[int] | None:
        """Convert value before send to db."""
        return value

    def to_python_value(
        self: typing.Self, value: typing.Any
    ) -> list[int] | None:
        """Convert db value to python."""
        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [int(x) for x in array]

        return None
