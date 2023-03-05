import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def load(self, collection_name, filter_data):
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

    def load(self, collection_name, filter_data=None):
        collection = self.mongo.database[collection_name]
        if filter_data is not None:
            return collection.find(filter_data)
        else:
            return collection.find()

    def update_flag(self, data):
        self.mongo.database.anime_links.find_one_and_update(
            {"_id": data["_id"]},
            {"$set": {"flag": True}}
        )


class FileStorage(StorageAbstract):
    @staticmethod
    def store(data, directory_name, file_name):
        with open(f"data/{directory_name}/{file_name}.json", "w") as f:
            f.write(json.dumps(data))
        print(f"data/anime{file_name}.json")

    def load(self, collection_name, filter_data=None):
        with open(f"data/{collection_name}/links.json", "r") as f:
            datas = json.loads(f.read())
        return datas

    def update_flag(self, data):
        pass
