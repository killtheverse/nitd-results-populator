import os
import pymongo
from dotenv import load_dotenv

load_dotenv()


class Database():
    uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_NAME")
    database = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.uri)
        Database.database = client[Database.database_name]
