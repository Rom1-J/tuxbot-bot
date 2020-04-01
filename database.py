import sqlalchemy
from utils.models import database, metadata
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--migrate", action="store_true")
parser.add_argument("-s", "--seed", action="store_true")
args = parser.parse_args()

if args.migrate:
    print("Migrate...")
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
    print("Done!")

if args.seed:
    print('Seeding...')
    # todo: add seeding
    print("Done!")
