import pymongo
from datetime import datetime
from functools import wraps
from flask import request
import config

# connect to the MongoDB server
client = pymongo.MongoClient(config.MONGO_URL)
db = client["endpoint_calls"]
collection = db["calls"]


# define the wrapper function
def log_endpoint_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get the current time and the endpoint URL
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = request.url

        # create a document to insert into the MongoDB collection
        document = {"timestamp": timestamp, "url": url}

        # insert the document into the collection
        result = collection.insert_one(document)

        # call the original function and return its result
        return func(*args, **kwargs)

    return wrapper
