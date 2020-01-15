import orm
from . import database, metadata


class AliasesModel(orm.Model):
    __tablename__ = 'aliases'
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    user_id = orm.String(max_length=18)
    alias = orm.String(max_length=255)
    command = orm.String(max_length=255)
    guild = orm.String(max_length=255)
