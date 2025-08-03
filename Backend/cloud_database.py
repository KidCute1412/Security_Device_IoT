from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()




client = MongoClient(os.getenv("MONGO_URI"))

# This is the DATABASE for the security device
db = client["security_device"]

# This is COLLECTIONS (equivalent to table in SQL) for the security device
user_account_collection = db["user_account"]
sensor_data_collection = db["sensor_data"]
alert_collection = db["alert"]


# Some constraints
user_account_collection.create_index("username", unique=True)

