from pymongo import MongoClient


class MongoDatabase:
    """
    A class to crate a MongoDB database which is singleton
    """
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:  # check if the class attribute instance is None
            # if it is None, create a new instance of the class
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        # create an instance variable called clint, which is an instance of the MongoClient class
        self.clint = MongoClient()
        # create an instance variable called database, which is the "crawler" database in MongoDB
        self.database = self.clint["crawler"]
