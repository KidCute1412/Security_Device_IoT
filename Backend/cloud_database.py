from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()




client = MongoClient(os.getenv("MONGO_URI"))

# This is the DATABASE for the security device
db = client["security_device"]

# This is COLLECTIONS (equivalent to table in SQL) for the security device

# format in user_account_collection:
# {
#     "_id": "ObjectId('...')",
#     "username": "user1",
#     "password": "hashed_password",
#     "email": ""
# }
user_account_collection = db["user_account"]


# format in sensor_data_collection: (only save to cloud when the value of sensor is true)
# {
#    "_id"  : "ObjectId('...')",
#    "user_id": "ObjectId('...')", (this is the id of user_account_collection)
#    "sensor_type": "sensor1", (pir sensor, vibration sensor)
#    "timestamp": ISODate("2023-10-01T12:00:00Z) # format in ISODate
# }
sensor_data_collection = db["sensor_data"]


# format in alert_collection: (save to cloud when all the value of sensor is true)
# {
#    "_id"  : "ObjectId('...')",
#    "user_id": "ObjectId('...')", (this is the id of user_account_collection)
#    "timestamp": ISODate("2023-10-01T12:00:00Z) # format in ISODate
# }

alert_collection = db["alert"]


# Some constraints
user_account_collection.create_index("username", unique=True)

