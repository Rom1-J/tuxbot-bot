"""
Big Int Array field specifically for PostgreSQL.

This field can store list of bigint values.
"""
import json
import typing

from tortoise.fields import Field
from tortoise.models import Model


class BigIntArrayField(Field[list[int]]):
    """
    Big Int Array field specifically for PostgreSQL.

    This field can store list of bigint values.
    """

    SQL_TYPE = "bigint[]"

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

    def to_db_value(
        self, value: list[int], instance: type[Model] | Model
    ) -> list[int] | None:
        """Convert value before send to db"""

        return value

    def to_python_value(self, value: typing.Any) -> list[int] | None:
        """Convert db value to python"""

        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [int(x) for x in array]

        return None
