import tortoise
from tortoise import fields


class Suggest(tortoise.Model):
    suggest_id = fields.BigIntField(pk=True)
    poll = fields.ForeignKeyField("models.Poll")
    user_id = fields.BigIntField()

    proposition = fields.CharField(max_length=30)

    class Meta:
        table = "suggests"

    def __str__(self):
        return (
            f"<suggest_id poll={self.poll} "
            f"user_id={self.user_id} "
            f"proposition={self.proposition}>"
        )

    __repr__ = __str__
