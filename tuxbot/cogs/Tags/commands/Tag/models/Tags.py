"""
Tags model
"""
from tortoise import Model, fields


class TagsModel(Model):
    """
    Tag Model used for tags command
    """

    id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField(description="Guild ID")
    author_id = fields.BigIntField(description="Author ID")

    name = fields.TextField()
    content = fields.TextField()

    uses = fields.IntField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True)

    # =========================================================================

    class Meta:
        """Meta values"""

        table = "tags"

    # =========================================================================

    def __str__(self):
        return (
            f"<Tag id={self.id} "
            f"guild_id={self.guild_id} "
            f"author_id={self.author_id} "
            f"name='{self.name}' "
            f"content='{self.content}' "
            f"uses={self.uses} "
            f"created_at={self.created_at}>"
        )

    __repr__ = __str__
