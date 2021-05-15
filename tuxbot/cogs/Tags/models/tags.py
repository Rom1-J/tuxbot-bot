import tortoise
from tortoise import fields


class Tag(tortoise.Model):
    id = fields.BigIntField(pk=True)
    server_id = fields.BigIntField()
    author_id = fields.BigIntField()

    name = fields.TextField()
    content = fields.TextField()

    uses = fields.IntField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tags"

    def __str__(self):
        return (
            f"<Tag id={self.id} "
            f"server_id={self.server_id} "
            f"author_id={self.author_id} "
            f"name='{self.name}' "
            f"content='{self.content}' "
            f"uses={self.uses} "
            f"created_at={self.created_at}>"
        )

    __repr__ = __str__
