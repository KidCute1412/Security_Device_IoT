import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import  request, jsonify
from Backend.cloud_database import user_account_collection, sensor_data_collection, alert_collection
import bcrypt
import Backend.global_vars as global_vars
from datetime import date, datetime
import Backend.global_vars as gv


# Login and Register API
login_success = False
def check_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Hash the password before checking
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Check if the username and hashed password match in the database
    if not username or not password:
        return False
    if user_account_collection is None or not user_account_collection:
        print("User account collection is not initialized.")
        return False
    if not user_account_collection.find_one({"username": username}):
        print(f"Username {username} does not exist.")
        return False
    
    print(f"Received login request with username: {username} and password: {password}")
    user = user_account_collection.find_one({"username": username})
    #Check password
    is_correct_password = False
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        print("Password matches.")
        is_correct_password = True
    else:
        print("Password does not match.")
        return False
    
    print(f"User found: {user}")
    if user and is_correct_password:
        return True
    else:
        return False

def get_user_info(username):
    user = user_account_collection.find_one({"username": username})

    if user:
        return {
            "username": user["username"],
            # "password": user["password"],
            "email": user["email"]
        }
    else:
        return None    
    
def login():
    global login_success
    if request.method == 'POST':
        login_success = check_login()
        if login_success:
            user_info = get_user_info(request.get_json().get('username'))
            if not user_info:
                return jsonify({"status": "ERROR", "message": "User not found"}), 404
            print(f"User info: {user_info}")
            user_name = user_info["username"]
            email = user_info["email"]

            # Update global variables
            global_vars.global_username = user_name
            global_vars.global_email = email
            global_vars.update_global_id()  # Update global ID based on username
            print(f"Global username: {global_vars.global_username}")
            print(f"Global email: {global_vars.global_email}")
            print(f"Global id: {global_vars.global_id}")
            return jsonify({"status": "OKE", "message": "Login successful", 
                            "username": user_name, "email": email}), 200
            # Send login notification email from a stationary account
            
        else:
            return jsonify({"status": "ERROR", "message": "Invalid username or password"}), 200
    else:
        return jsonify({"status": "ERROR", "message": "Method not allowed"}), 405    


# Sign-up API
# Helper function to send email from a stationary account
def send_register_email(recipient_email, username):
    # Stationary sender account credentials
    sender_email = "lykhai2520@gmail.com"  # Replace with your stationary email
    sender_password = "uedq tldh ixxj iyak"  # Replace with your app password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = "SIGN-UP Notification"
    body = f"Hello {username},\n\nYou have successfully signed up your account.\n\nIf this wasn't you, please secure your account immediately.\n\nBest regards,\nSecurity Device IoT Team"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def send_logout_email(recipient_email, username):
    sender_email = "lykhai2520@gmail.com"  # Replace with your stationary email
    sender_password = "uedq tldh ixxj iyak"  # Replace with your app password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = "Logout Notification"
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date.replace(hour=23, minute=59, second=59)
    alerts = alert_collection.find({"user_id": gv.global_id, 
                                    "timestamp": {"$gte": start_date, 
                                                  "$lt": end_date}})
    if alerts.count() == 0:
        body = f"Hello {username},\n\nYou have successfully logged out of your account.\n\nNo alerts were triggered during today.\n\nBest regards,\nSecurity Device IoT Team"
    else:
        body = f"Hello {username},\n\nYou have successfully logged out of your account.\n\nYou had {alerts.count()} alerts triggered today.\n\nBest regards,\nSecurity Device IoT Team"
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def is_valid_email(email):
    # Check if the email is valid (simple regex check)
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

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
    email = data.get('email')
    # Normalize inputs
    username = normalize_username(username)
    print(f"Received sign-up request with username: {username} and password: {password} and email: {email}")
    # Vali date inputs
    if not check_existed_username(username) and valid_password(password) and len(username) != 0 and is_valid_email(email):

        # Hash the password before storing it
  
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert new user into the database
        user_account_collection.insert_one({
            "username": username,
            "password": hashed_password.decode('utf-8'),
            "email": email
        })
        try:
            send_register_email(email, username)
        except Exception as e:
            print(f"[EMAIL ERROR] Could not send login email: {e}")
        return jsonify({"status": "OKE", "message": "Sign-up successful"}), 201
    else:
        # Return error response if validation fails
        if len(username) == 0:
            return jsonify({"status": "ERROR", "message": "Username is empty"}), 400
        if not valid_password(password):
            return jsonify({"status": "ERROR", "message": "Password is not valid"}), 400
        if not is_valid_email(email):
            return jsonify({"status": "ERROR", "message": "Email is not valid"}), 400
        if check_existed_username(username):
            return jsonify({"status": "ERROR", "message": "Username already exists"}), 400
        
        
    
