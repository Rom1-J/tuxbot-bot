import databases
import sqlalchemy
from utils.functions import Config

conf_postgresql = Config('./configs/config.cfg')["postgresql"]
postgresql = 'postgresql://{}:{}@{}/{}'.format(
    conf_postgresql.get("Username"), conf_postgresql.get("Password"),
    conf_postgresql.get("Host"), conf_postgresql.get("DBName"))

database = databases.Database(postgresql)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)

from .warn import WarnModel
from .poll import PollModel, ResponsesModel
from .alias import AliasesModel
