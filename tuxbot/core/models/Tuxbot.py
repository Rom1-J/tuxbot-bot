"""
Tuxbot model
"""
from tortoise import fields
from tortoise.models import Model

from tuxbot.core.models.fields.BigIntArrayField import BigIntArrayField


class TuxbotModel(Model):
    """
    Tuxbot Model used to store tuxbot configs
    """

    id = fields.BigIntField(pk=True, description="Client ID")
    prefix = fields.TextField(default=".", description="Tuxbot prefix")

    ignored_users = BigIntArrayField(
        description="Tuxbot ignored users", default=None, null=True
    )
    ignored_channels = BigIntArrayField(
        description="Tuxbot ignored channels", default=None, null=True
    )
    ignored_guilds = BigIntArrayField(
        description="Tuxbot ignored guilds", default=None, null=True
    )

    # =========================================================================

    class Meta:
        """Meta values"""

        table = "tuxbot"

    # =========================================================================
