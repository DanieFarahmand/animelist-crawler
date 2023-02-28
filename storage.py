import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, collection_name, *args):
        collection = getattr(self.mongo.database, collection_name)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)


class FileStorage(StorageAbstract):
    @staticmethod
    def store(data, directory_name, file_name):
        with open(f"data/{directory_name}/{file_name}.json", "w") as f:
            f.write(json.dumps(data))
        print(f"data/anime{file_name}.json")
