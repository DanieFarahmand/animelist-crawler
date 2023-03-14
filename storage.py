import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):
    """
    Define an abstract class `StorageAbstract` with abstract methods `store` and `load`
    """

    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def load(self, collection_name, filter_data):
        pass


class MongoStorage(StorageAbstract):
    """
    Define a class `MongoStorage` that implements the `StorageAbstract` abstract class
    to load and store the datas in MongoDB
    """

    def __init__(self):
        # Create a new instance of the `MongoDatabase` class to connect to a MongoDB database
        self.mongo = MongoDatabase()

    def store(self, data, collection_name, *args):
        # Get the collection from the connected MongoDB database
        collection = getattr(self.mongo.database, collection_name)
        # If `data` is a list and has more than one element, insert all elements into the collection
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        # If `data` is a single element, insert it into the collection
        else:
            collection.insert_one(data)

    def load(self, collection_name, filter_data=None):
        # Get the collection from the connected MongoDB database
        collection = self.mongo.database[collection_name]
        # If `filter_data` is provided, return all documents in the collection
        if filter_data is not None:
            return collection.find(filter_data)
        # If `filter_data` is not provided, return all documents in the collection
        else:
            return collection.find()

    def update_flag(self, data):
        """
        Define an additional method `update_flag` to update the `flag` field of
        a specific document in the `anime_links` collection.
        """
        self.mongo.database.anime_links.find_one_and_update(
            {"_id": data["_id"]},
            {"$set": {"flag": True}}
        )


class FileStorage(StorageAbstract):
    """
    Define a class `FileStorage` that implements the `StorageAbstract` abstract class
    to load and store the datas in local files
    """

    @staticmethod
    def store(data, directory_name, file_name):
        with open(f"data/{directory_name}/{file_name}.json", "w") as f:
            f.write(json.dumps(data))
        print(f"data/anime{file_name}.json")

    def load(self, collection_name, filter_data=None):
        """
        Implement the `load` method to retrieve data from a JSON file.
        """
        with open(f"data/{collection_name}/links.json", "r") as f:
            datas = json.loads(f.read())
        return datas

    def update_flag(self, data):
        """
        Define a method `update_flag` that does nothing for this class, since there
        is no document to update in a JSON file.
        """
        pass
