from utils import Config
from utils import Database

database = Database(Config("./configs/config.cfg"))

Base.metadata.create_all(database.engine)
