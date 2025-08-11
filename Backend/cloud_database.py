from pymongo import MongoClient
import os
from dotenv import load_dotenv
import Backend.global_vars as glb
from datetime import datetime, timezone
import threading

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
    
    
    utc_timestamp = datetime.now() # local time
    print(f"Timestamp: {utc_timestamp}")
    
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
    utc_timestamp = datetime.now()
    print(f"Timestamp: {utc_timestamp}")
    
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



def update_data_to_cloud():
    while True:
        try:
            # Save alert if both sensors are triggered
            if (glb.tmp_pir_sensor and glb.tmp_vibration_sensor) and\
            (not glb.current_pir_sensor or not glb.current_vibration_sensor):
                save_alert()

            # Save sensor data if the sensors are triggered
            if glb.tmp_pir_sensor != glb.current_pir_sensor:
                if glb.tmp_pir_sensor: # Tmp True but current False
                    save_sensor_data("pir_sensor")
                glb.current_pir_sensor = glb.tmp_pir_sensor
            
            if glb.tmp_vibration_sensor != glb.current_vibration_sensor:
                if glb.tmp_vibration_sensor: # Tmp True but current False
                    save_sensor_data("vibration_sensor")
                glb.current_vibration_sensor = glb.tmp_vibration_sensor

            # Sleep for a while before the next check
            threading.Event().wait(1)  # Adjust the interval as needed
        except Exception as e: 
            print(f"Error in update_data_to_cloud: {e}")



def start_update_thread():
    """
    Start a background thread to update data to the cloud.
    """
    update_thread = threading.Thread(target=update_data_to_cloud)
    update_thread.daemon = True  # Daemonize thread
    update_thread.start()
    print("Background thread for updating data to cloud started.")
