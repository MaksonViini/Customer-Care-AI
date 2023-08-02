from pymongo import MongoClient

from .config import get_db_url

DB_URL = get_db_url()


client = MongoClient(DB_URL)
database = client["customer-care-db"]


script_collection = database["script"]
users_collection = database["users"]
conversations_collection = database["messages"]
