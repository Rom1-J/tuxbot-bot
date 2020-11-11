import tortoise
from tortoise import fields


class Poll(tortoise.Model):
    id = fields.BigIntField(pk=True)
    channel_id = fields.BigIntField()
    message_id = fields.BigIntField()
    author_id = fields.BigIntField()

    content = fields.JSONField()
    is_anonymous = fields.BooleanField()

    available_choices = fields.IntField()

    choices: fields.ManyToManyRelation["Response"] = fields.ManyToManyField(
        "models.Response", related_name="choices"
    )

    class Meta:
        table = "polls"

    def __str__(self):
        return (
            f"<Poll id={self.id} "
            f"channel_id={self.channel_id} "
            f"message_id={self.message_id} "
            f"author_id={self.author_id} "
            f"content={self.content} "
            f"is_anonymous={self.is_anonymous} "
            f"available_choices={self.available_choices} "
            f"choices={self.choices}>"
        )

    __repr__ = __str__
