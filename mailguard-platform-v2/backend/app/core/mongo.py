from pymongo import MongoClient

from app.core.config import settings

_mongo_client = None


# Kthen databazen MongoDB (klienti krijohet vetem njehere dhe riperdoret)
def get_mongo_database():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
    return _mongo_client[settings.MONGODB_DATABASE]
