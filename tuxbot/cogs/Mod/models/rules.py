import tortoise
from tortoise import fields


class Rule(tortoise.Model):
    id = fields.BigIntField(pk=True)
    server_id = fields.BigIntField()
    author_id = fields.BigIntField()
    rule_id = fields.IntField()
    content = fields.TextField(max_length=300)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "rules"

    def __str__(self):
        return (
            f"<Rule id={self.id} "
            f"server_id={self.server_id} "
            f"author_id={self.author_id} "
            f"rule_id={self.rule_id} "
            f"content='{self.content}' "
            f"created_at={self.created_at} "
            f"updated_at={self.updated_at}>"
        )

    __repr__ = __str__
