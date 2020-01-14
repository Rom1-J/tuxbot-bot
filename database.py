from utils import Config
from utils.models import Base
from utils import Database
from utils.models.lang import LangModel
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--migrate", action="store_true")
parser.add_argument("-s", "--seed", action="store_true")
args = parser.parse_args()

database = Database(Config("./configs/config.cfg"))

if args.migrate:
    print("Migrate...")
    Base.metadata.create_all(database.engine)
    print("Done!")

if args.seed:
    print('Seeding...')
    default = LangModel(key="default", value="fr")
    available = LangModel(key="available", value="fr,en")

    database.session.add(default)
    database.session.add(available)

    database.session.commit()
    print("Done!")
