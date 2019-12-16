from cogs.utils.models import *
from cogs.utils.config import Config
from cogs.utils.database import Database

database = Database(Config("./configs/config.cfg"))

Base.metadata.create_all(database.engine)
