from tortoise import Model, fields

from .Choices import ChoicesModel


class PollsModel(Model):
    id = fields.BigIntField(pk=True)

    channel_id = fields.BigIntField(description="Channel ID")
    message_id = fields.BigIntField(description="Message ID")
    author_id = fields.BigIntField(description="Author ID")

    message = fields.CharField(description="Poll message", max_length=256)

    created_at = fields.DatetimeField(auto_now_add=True)

    # =========================================================================

    choices: fields.ReverseRelation[ChoicesModel]

    # =========================================================================

    class Meta:
        """Meta values"""

        table = "polls_message"

    # =========================================================================

    def __str__(self):
        return (
            f"<Poll id={self.id} "
            f"channel_id={self.channel_id} "
            f"message_id={self.message_id} "
            f"author_id={self.author_id} "
            f"message='{self.message}' "
            f"created_at={self.created_at}>"
        )

    __repr__ = __str__
