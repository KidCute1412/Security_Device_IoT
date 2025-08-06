import Backend.cloud_database as cloud
from bson.objectid import ObjectId
global_username = None
global_email = None
global_id = None
global_id = ObjectId("68902f6941cf03cf917bf9de")  # Default value, will be updated later
current_pir_sensor = None
current_vibration_sensor = None
current_led_status = None
current_buzzer_status = None
current_lcd_status = None

tmp_pir_sensor = False  # Temporary variable to store sensor data
tmp_vibration_sensor = False  # Temporary variable to store sensor data




def update_global_id():
    global global_id
    if cloud.user_account_collection:
        user = cloud.user_account_collection.find_one({"username": global_username})
        if user:
            global_id = user.get("_id")
            print(f"Global ID updated: {global_id}")
            print(f"Global ID type: {type(global_id)}")
        else:
            global_id = None
