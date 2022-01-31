"""
Big Int Array field specifically for PostgreSQL.

This field can store list of bigint values.
"""
import json
from typing import List, Union, Type, Optional, Any

from tortoise import Model
from tortoise.fields import Field


class BigIntArrayField(Field, list):
    """
    Big Int Array field specifically for PostgreSQL.

    This field can store list of bigint values.
    """

    SQL_TYPE = "bigint[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(
        self, value: List[int], instance: Union[Type[Model], Model]
    ) -> Optional[List[int]]:
        """Convert value before send to db"""

        return value

    def to_python_value(self, value: Any) -> Optional[List[int]]:
        """Convert db value to python"""

        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [int(x) for x in array]

        return value
