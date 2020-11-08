import tortoise
from tortoise import fields


class AliasesModel(tortoise.Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    alias = fields.TextField(max_length=255)
    command = fields.TextField(max_length=255)
    guild = fields.BigIntField()

    class Meta:
        table = "aliases"

    def __str__(self):
        return f"<AliasesModel id={self.id} " \
               f"user_id={self.user_id} " \
               f"alias='{self.alias}' " \
               f"command='{self.command}' " \
               f"guild={self.guild}>"

    __repr__ = __str__
