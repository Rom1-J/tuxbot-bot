import tortoise
from tortoise import fields


class MuteRole(tortoise.Model):
    id = fields.BigIntField(pk=True)
    server_id = fields.BigIntField()
    role_id = fields.BigIntField()

    class Meta:
        table = "mute_role"

    def __str__(self):
        return (
            f"<MuteRole id={self.id} "
            f"server_id={self.server_id} "
            f"role_id={self.role_id}>"
        )

    __repr__ = __str__


class Mute(tortoise.Model):
    id = fields.BigIntField(pk=True)
    server_id = fields.BigIntField()
    author_id = fields.BigIntField()
    reason = fields.TextField(max_length=300)
    member_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    expire_at = fields.DatetimeField(null=True)

    class Meta:
        table = "mutes"

    def __str__(self):
        return (
            f"<Mute id={self.id} "
            f"server_id={self.server_id} "
            f"author_id={self.author_id} "
            f"reason='{self.reason}' "
            f"member_id={self.member_id} "
            f"created_at={self.created_at} "
            f"expire_at={self.expire_at}>"
        )

    __repr__ = __str__
