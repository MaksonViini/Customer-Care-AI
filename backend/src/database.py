from pymongo import MongoClient

from .config import get_db_url

DB_URL = get_db_url()

client = MongoClient("localhost", 27017)
database = client["teste_data"]


script_collection = database["script"]
description_colletion = database["description"]
users_collection = database["users"]
conversations_collection = database["bot"]


# def update(args):
#     try:
#         collection.update_one(args[0], args[1])
#     except Exception:
#         return False


# def delete(args):
#     try:
#         collection.delete_one(args)
#     except Exception:
#         return False


# def delete_(args):
#     try:
#         collection.delete_many(args)
#     except Exception:
#         return False
