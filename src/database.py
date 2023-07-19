from motor.motor_asyncio import AsyncIOMotorClient

from .config import Settings

settings = Settings(config={"env": "dev"}).config

DB_URL = f"""mongodb://root:{settings.db_password}
@{settings.db_host}:{settings.db_port}/"""

client = AsyncIOMotorClient(DB_URL)
database = client["teste_data"]
collection = database["bot"]


def insert(**args):
    try:
        collection.insert_one(args)
    except Exception:
        return False


def read(**args):
    try:
        return collection.find(args)
    except Exception:
        return False


def update(args):
    try:
        collection.update_one(args[0], args[1])
    except Exception:
        return False


def delete(args):
    try:
        collection.delete_one(args)
    except Exception:
        return False


def delete_(args):
    try:
        collection.delete_many(args)
    except Exception:
        return False
