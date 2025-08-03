import Backend.cloud_database as cloud
from bson.objectid import ObjectId
global_username = None
global_email = None
global_id = None

current_pir_sensor = None
current_vibration_sensor = None
current_led_status = None
current_buzzer_status = None
current_lcd_status = None





def update_global_id():
    global global_id
    if cloud.user_account_collection:
        user = cloud.user_account_collection.find_one({"username": global_username})
        if user:
            global_id = user.get("_id")
        else:
            global_id = None
