import tortoise
from tortoise import fields


class WarnsModel(tortoise.Model):
    id = fields.BigIntField(pk=True)
    server_id = fields.BigIntField()
    user_id = fields.BigIntField()
    reason = fields.TextField(max_length=255)
    created_at = fields.DatetimeField()

    class Meta:
        table = "warns"

    def __str__(self):
        return f"<WarnsModel id={self.id} " \
               f"server_id={self.server_id} " \
               f"user_id={self.user_id} " \
               f"reason='{self.reason}' " \
               f"created_at={self.created_at}>"

    __repr__ = __str__
