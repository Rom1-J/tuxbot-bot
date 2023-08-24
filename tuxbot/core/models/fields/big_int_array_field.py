"""
Big Int Array field specifically for PostgreSQL.

This field can store list of bigint values.
"""
import typing
from enum import Enum

from tortoise.fields import Field
from tortoise.models import Model
from tortoise.validators import Validator


class _KwargsT(typing.TypedDict):
    source_field: str | None
    generated: bool
    pk: bool
    null: bool
    default: typing.Any
    unique: bool
    index: bool
    description: str | None
    model: Model | None
    validators: list[Validator | typing.Callable] | None


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
    ) -> list[int | Enum]:
        """Convert db value to python."""
        return value
