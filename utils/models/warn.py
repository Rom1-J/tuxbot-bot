import orm
from . import database, metadata


class WarnModel(orm.Model):
    __tablename__ = 'warns'
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    server_id = orm.String(max_length=18)
    user_id = orm.String(max_length=18)
    reason = orm.String(max_length=255)
    created_at = orm.DateTime()
