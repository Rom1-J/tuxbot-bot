import tortoise
from tortoise import fields


class AutoBan(tortoise.Model):
    id = fields.BigIntField(pk=True)
    server_id = fields.BigIntField()

    reason = fields.TextField(max_length=300)
    match = fields.TextField(max_length=20)
    log_channel = fields.BigIntField(null=True)

    class Meta:
        table = "autobans"

    def __str__(self):
        return (
            f"<AutoBan id={self.id} "
            f"server_id={self.server_id} "
            f"reason='{self.reason}' "
            f"match='{self.match}' "
            f"log_channel={self.log_channel}>"
        )

    __repr__ = __str__
