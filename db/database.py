import os
import pymongo
import logging
from dotenv import load_dotenv

load_dotenv()


class Database():
    uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_NAME")
    database = None

    @staticmethod
    def initialize():
        logging.info("Establishing Database connection")
        client = pymongo.MongoClient(Database.uri)
        logging.info("Database connection established")
        Database.database = client[Database.database_name]
