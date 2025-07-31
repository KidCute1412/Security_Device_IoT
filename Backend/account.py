from flask import  request, jsonify
from Backend.cloud_database import user_account_collection 


# Simulate account





# Login and Register API

def check_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(f"Received login request with username: {username} and password: {password}")
    user = user_account_collection.find_one({"username": username, "password": password})
    if user:
        return True
    else:
        return False

def get_user_info(username):
    user = user_account_collection.find_one({"username": username})
    if user:
        return {
            "username": user["username"],
            "phone_number": user["phone_number"],
            "password": user["password"]    
        }
    else:
        return None    
def login():
    if request.method == 'POST':
        if check_login():
            user_info = get_user_info(request.get_json().get('username'))
            if not user_info:
                return jsonify({"status": "ERROR", "message": "User not found"}), 404
            print(f"User info: {user_info}")
            user_name, phone_number, password = user_info["username"], user_info["phone_number"], user_info["password"]
            return jsonify({"status": "OKE", "message": "Login successful", 
                            "username": user_name, "phone_number": phone_number,
                            "password": password}), 200
        else:
            return jsonify({"status": "ERROR", "message": "Invalid username or password"}), 401
    else:
        return jsonify({"status": "ERROR", "message": "Method not allowed"}), 405    


# Sign-up API

def normalize_phone_number(phone):
    # Normalize phone number to ensure it has 10 digits
    return ''.join(filter(str.isdigit, phone))[-10:]

def normalize_username(username):
    # Normalize username to ensure it is a valid string
    return "".join(username.split()).lower()

def valid_password(password):
    number = 0
    special_characters = "!@#$%^&*()-_=+[]{}|;:',.<>?/"
    number_special_characters = 0
    number_alphabet = 0
    for char in password:
        if char.isdigit():
            number += 1
        elif char in special_characters:
            number_special_characters += 1
        elif char.isalpha():
            number_alphabet += 1
    return number >= 1 and number_special_characters >= 1 and number_alphabet >= 1 and len(password) >= 3       
        
def check_existed_username(username):
    # Check if the username already exists in the database
    return user_account_collection.find_one({"username": username}) is not None

def sign_up():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone_number')
    # Normalize inputs
    username = normalize_username(username)
    phone = normalize_phone_number(phone)
    print(f"Received sign-up request with username: {username} and password: {password}"
          and f" phone: {phone}")
    # Validate inputs
    if not check_existed_username(username) and valid_password(password) and len(phone) == 10 and len(username) != 0:

        # Insert new user into the database
        user_account_collection.insert_one({
            "username": username,
            "password": password,
            "phone_number": phone
        })
        # Return success response to frontend
        return jsonify({"status": "OKE", "message": "Sign-up successful"}), 201
    else:
        # Return error response if validation fails
        if len(username) == 0:
            return jsonify({"status": "ERROR", "message": "Username is empty"}), 400
        if not valid_password(password):
            return jsonify({"status": "ERROR", "message": "Password is not valid"}), 400
        if len(phone) != 10:
            return jsonify({"status": "ERROR", "message": "Phone number is not valid"}), 400
        if check_existed_username(username):
            return jsonify({"status": "ERROR", "message": "Username already exists"}), 400
        
        
    
