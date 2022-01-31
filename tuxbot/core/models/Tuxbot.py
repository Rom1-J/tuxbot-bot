"""
Tuxbot model
"""
from tortoise import Model, fields

from tuxbot.core.models.fields.BigIntArrayField import BigIntArrayField


class TuxbotModel(Model):
    """
    Tuxbot Model used to store tuxbot configs
    """

    id = fields.BigIntField(pk=True, description="Client ID")
    prefix = fields.TextField(default=".", description="Tuxbot prefix")

    ignored_users = BigIntArrayField(description="Tuxbot ignored users")
    ignored_channels = BigIntArrayField(description="Tuxbot ignored channels")
    ignored_guilds = BigIntArrayField(description="Tuxbot ignored guilds")

    # =========================================================================

    class Meta:
        """Meta values"""
        table = "tuxbot"

    # =========================================================================
