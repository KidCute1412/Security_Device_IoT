from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()




client = MongoClient(os.getenv("MONGO_URI"))

# This is the DATABASE for the security device
db = client["security_device"]

# This is COLLECTIONS (equivalent to table in SQL) for the security device
user_account_collection = db["user_account"]


# Some constraints
user_account_collection.create_index("username", unique=True)

