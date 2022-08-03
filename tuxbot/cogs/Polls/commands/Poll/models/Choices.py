from tortoise import Model, fields


class ChoicesModel(Model):
    id = fields.BigIntField(pk=True)

    poll = fields.ForeignKeyField(
        "models.PollsModel", on_delete=fields.CASCADE, related_name="choices"
    )

    choice = fields.CharField(description="Poll choice", max_length=256)
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
