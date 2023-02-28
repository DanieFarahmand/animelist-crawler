import json
from abc import ABC, abstractmethod


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass


class MongoStorage:
    pass


class FileStorage(StorageAbstract):
    @staticmethod
    def store(data, directory_name, file_name):
        with open(f"data/{directory_name}/{file_name}.json", "w") as f:
            f.write(json.dumps(data))
        print(f"data/anime{file_name}.json")
