from pymongo import MongoClient

from app.core.config import settings

_client = None


# Kthen lidhjen me MongoDB (nje klient i vetem, i ripërdorur)
def get_mongo_db():
    # Klienti krijohet vetem njehere dhe ripordoret
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
    return _client[settings.MONGODB_DATABASE]
