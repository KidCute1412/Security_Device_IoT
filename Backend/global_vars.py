import Backend.cloud_database as cloud
from bson.objectid import ObjectId
global_username = None
global_email = None
global_id = None






def update_global_id():
    global global_id
    if cloud.user_account_collection:
        user = cloud.user_account_collection.find_one({"username": global_username})
        if user:
            global_id = user.get("_id")
        else:
            global_id = None