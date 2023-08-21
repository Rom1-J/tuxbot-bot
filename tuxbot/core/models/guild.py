"""Guild model."""
import typing

from tortoise import fields
from tortoise.models import Model

from tuxbot.core.models.fields.big_int_array_field import BigIntArrayField


class GuildModel(Model):
    """Guild Model used to store guild configs."""

    id = fields.BigIntField(pk=True, description="Guild ID")  # noqa: A003
    prefix = fields.TextField(default=".", description="Guild prefix")

    moderators = BigIntArrayField(
        description="Guild moderators", default=None, null=True
    )
    moderator_roles = BigIntArrayField(
        description="Guild moderator roles", default=None, null=True
    )

    deleted = fields.BooleanField(
        default=True, description="Either the bot is on this guild"
    )

    # =========================================================================

    class Meta:
        """Meta values."""

        table = "guild"

    # =========================================================================

    def __str__(self: typing.Self) -> str:
        return str(self.id)

    def __repr__(self: typing.Self) -> str:
        return f"<Guild id={self.id}>"
