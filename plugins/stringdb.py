import pymongo
import random
import string
from config import DB_URI

# Connect to MongoDB
client = pymongo.MongoClient(DB_URI)
db = client["string_mapping_db"]
collection = db["string_mapping"]

def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))

def save_mapping(random_string, original_string):
    mapping = {"random_string": random_string, "original_string": original_string}
    collection.insert_one(mapping)

def get_original_string(random_string):
    mapping = collection.find_one({"random_string": random_string})
    return mapping["original_string"] if mapping else None

