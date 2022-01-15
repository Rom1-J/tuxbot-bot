import tortoise
from tortoise import fields


class Suggest(tortoise.Model):
    suggest_id = fields.BigIntField(pk=True)
    poll = fields.ForeignKeyField("models.Poll")
    channel_id = fields.BigIntField()
    message_id = fields.BigIntField()
    author_id = fields.BigIntField()

    proposition = fields.CharField(max_length=30)

    class Meta:
        table = "suggests"

    def __str__(self):
        return (
            f"<suggest_id poll={self.poll} "
            f"author_id={self.author_id} "
            f"proposition={self.proposition}>"
        )

    __repr__ = __str__
