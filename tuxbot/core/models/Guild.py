"""
Guild model
"""
from tortoise import fields
from tortoise.models import Model

from tuxbot.core.models.fields.BigIntArrayField import BigIntArrayField


class GuildModel(Model):
    """
    Guild Model used to store guild configs
    """

    id = fields.BigIntField(pk=True, description="Guild ID")
    prefix = fields.TextField(default=".", description="Guild prefix")

    moderators = BigIntArrayField(description="Guild moderators")
    moderator_roles = BigIntArrayField(description="Guild moderator roles")

    deleted = fields.BooleanField(
        default=True, description="Either the bot is on this guild"
    )

    # =========================================================================

    class Meta:
        """Meta values"""

        table = "guild"

    # =========================================================================

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return f"<Server id={self.id}>"
