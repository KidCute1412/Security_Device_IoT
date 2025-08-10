from pymongo import MongoClient
import os
from dotenv import load_dotenv
import Backend.global_vars as glb
from datetime import datetime, timezone

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
#    "sensor_type": "sensor1", (pir, vibration)
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





# Data from esp32 to cloud

def save_sensor_data(sensor_type):
    if not glb.global_id:
        print("Global ID is not set. Cannot save sensor data.")
        return False
    
    # Get current UTC timestamp - modern way (recommended)
    utc_timestamp = datetime.now(timezone.utc)
    print(f"UTC Timestamp: {utc_timestamp}")
    
    data = {
        "user_id": glb.global_id,
        "sensor_type": sensor_type,
        "timestamp": utc_timestamp
    }
    
    try:
        sensor_data_collection.insert_one(data)
        print(f"Sensor data saved: {data}")
        return True
    except Exception as e:
        print(f"Error saving sensor data: {e}")
        return False

def save_alert():
    if not glb.global_id:
        print("Global ID is not set. Cannot save alert.")
        return False
    
    # Get current UTC timestamp - modern way (recommended)
    utc_timestamp = datetime.now(timezone.utc)
    print(f"UTC Timestamp: {utc_timestamp}")
    
    data = {
        "user_id": glb.global_id,
        "timestamp": utc_timestamp
    }
    
    try:
        alert_collection.insert_one(data)
        print(f"Alert saved: {data}")
        return True
    except Exception as e:
        print(f"Error saving alert: {e}")
        return False



