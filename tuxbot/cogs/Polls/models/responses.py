import tortoise
from tortoise import fields


class Response(tortoise.Model):
    response_id = fields.BigIntField(pk=True)
    poll = fields.ForeignKeyField("models.Poll")
    user_id = fields.BigIntField()

    choice = fields.IntField()

    class Meta:
        table = "responses"

    def __str__(self):
        return (
            f"<Response poll={self.poll} "
            f"user_id={self.user_id} "
            f"choice={self.choice}>"
        )

    __repr__ = __str__
