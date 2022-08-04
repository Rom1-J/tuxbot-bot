from tortoise import Model, fields


class ChoicesModel(Model):
    id = fields.BigIntField(pk=True)

    poll = fields.ForeignKeyField(
        "models.PollsModel", on_delete=fields.CASCADE, related_name="choices"
    )

    label = fields.CharField(description="Choice label", max_length=8)
    choice = fields.CharField(description="Choice value", max_length=256)
    checked = fields.IntField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True)

    # =========================================================================

    class Meta:
        """Meta values"""

        table = "polls_choices"

    # =========================================================================

    def __str__(self):
        return (
            f"<Choice id={self.id} "
            f"poll={self.poll} "
            f"choice='{self.choice}' "
            f"checked={self.checked} "
            f"created_at={self.created_at}>"
        )

    __repr__ = __str__
