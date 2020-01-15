import orm
from . import database, metadata


class ResponsesModel(orm.Model):
    __tablename__ = 'responses'
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    user = orm.String(max_length=18)

    choice = orm.Integer()


class PollModel(orm.Model):
    __tablename__ = 'polls'
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    channel_id = orm.String(max_length=18)
    message_id = orm.String(max_length=18)

    content = orm.JSON()
    is_anonymous = orm.Boolean()

    available_choices = orm.Integer()
    choice = orm.ForeignKey(ResponsesModel)
