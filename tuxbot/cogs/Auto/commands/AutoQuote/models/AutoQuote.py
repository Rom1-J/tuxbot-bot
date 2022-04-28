"""
AutoQuote model
"""
from tortoise import Model, fields


class AutoQuoteModel(Model):
    """
    AutoQuote Model used for auto_quote command
    """

    id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField(description="Guild ID")

    activated = fields.BooleanField(default=False)

    # =========================================================================

    class Meta:
        """Meta values"""

        table = "auto_quote"

    # =========================================================================

    def __str__(self):
        return (
            f"<AutoQuote id={self.id} "
            f"guild_id={self.guild_id} "
            f"activated={self.activated}>"
        )

    __repr__ = __str__
