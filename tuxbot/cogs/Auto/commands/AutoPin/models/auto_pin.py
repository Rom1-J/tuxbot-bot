"""AutoPin model."""
import typing

from tortoise import fields
from tortoise.models import Model


class AutoPinModel(Model):
    """AutoPin Model used for auto_pin command."""

    id = fields.BigIntField(pk=True)  # noqa: A003
    guild_id = fields.BigIntField(description="Guild ID")

    activated = fields.BooleanField(default=False)
    threshold = fields.IntField(default=999_999_999)

    # =========================================================================

    class Meta:
        """Meta values."""

        table = "auto_pin"

    # =========================================================================

    def __str__(self: typing.Self) -> str:
        return (
            f"<AutoPin id={self.id} "
            f"guild_id={self.guild_id} "
            f"activated={self.activated} "
            f"threshold={self.threshold}>"
        )

    __repr__ = __str__
