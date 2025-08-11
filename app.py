from flask import Flask, redirect, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
import random
import Backend.account as account
import paho.mqtt.client as mqtt
import Backend.mqtt_communication as mqtt
import Backend.global_vars as glb
import Backend.cloud_database as cloud
import Backend.account as account

import Backend.gemini_api as gemini_api
import Backend.filter_data as filter_data
import Backend.chatbot as chatbot
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# # Bonus function
# def simulate_sensor():
#    # Simulate sensor data
#    reed_sensor = random.choice([True, False])
#    pir_sensor = random.choice([True, False])
#    vibration_sensor = random.choice([True, False])

#    return reed_sensor, pir_sensor, vibration_sensor
# Initial page
@app.route('/')
def first_page():
   if not glb.global_successfully_connected:
    return redirect("/Frontend/HTML/login.html")
   else:
    return redirect("/Frontend/HTML/dashboard.html")
@app.route('/Frontend/<path:filename>')
def serve_frontend(filename):
    return send_from_directory('Frontend', filename)


# API for getting all status
@app.route('/api/get_all_status', methods=['GET'])
def get_all_status():
    """
    Get all current device and sensor status via MQTT
    This function is called only when someone makes a GET request to /api/get_all_status
    """
    try:
        # This will return current global variables from MQTT
        import Backend.global_vars as glb
        
        return jsonify({
            "status": "OKE",
            "message": "All status retrieved successfully",
            "pir_status": glb.current_pir_sensor,
            "vibration_status": glb.current_vibration_sensor,
            "led_status": glb.current_led_status,
            "buzzer_status": glb.current_buzzer_status,
            "lcd_status": glb.current_lcd_status
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": f"Error getting status: {str(e)}"
        }), 500


# API for controlling devices

@app.route('/api/control_devices', methods=['POST'])
def control_devices():
    return mqtt.command_to_devices()

# API for login
@app.route('/api/login', methods=['POST'])
def login_process():
    # Call the login function
    result = account.login()
    
    # Check if login was successful and call unification
    if account.login_success:
        print("Login success:", account.login_success)
        try:
            mqtt.unification()
            mqtt.setup_mqtt_subscription()
            print("MQTT unification sent successfully")
        except Exception as e:
            print(f"Error sending MQTT unification: {e}")
    else:
        print("Login failed:", account.login_success)
    
    return result

# API for first chart
@app.route('/api/alerts_per_day', methods=['GET'])
def alerts_per_day():
    return filter_data.get_alerts_per_day()

# API for second chart
@app.route('/api/alerts_per_hour', methods=['GET'])
def alerts_per_hour():
    return filter_data.get_alerts_per_hour()

# API for logout
@app.route('/api/logout', methods=['POST'])
def logout():
    """
    Handle user logout by clearing global variables and redirecting to login page.
    """
    try:
        account.send_logout_email(glb.global_email, glb.global_username)
    except Exception as e:
        print(f"[EMAIL ERROR] Could not send logout email: {e}")
    glb.global_username = None
    glb.global_email = None
    glb.global_id = None
    glb.current_pir_sensor = None
    glb.current_vibration_sensor = None
    glb.current_led_status = None
    glb.current_buzzer_status = None
    glb.current_lcd_status = None
    glb.global_successfully_connected = False  # Reset connection flag
    
    print("User logged out successfully.")
    
    return jsonify({"status": "OKE", "message": "Logout successful"}), 200    


# API for register
@app.route('/api/sign-up', methods=['POST'])
def sign_up():
   return account.sign_up()




# API for password analysis (demo AI)
@app.route('/api/analyze_password_strength', methods=['GET'])

def analyze_password_strength():
   return gemini_api.analyze_password_strength()

# API for get date filter
# chart 1
@app.route('/api/get_date_chart1', methods=['POST'])
def get_date_chart1():
    return filter_data.get_date_chart1()
# chart 2
@app.route('/api/get_date_chart2', methods=['POST'])
def get_date_chart2():
    return filter_data.get_date_chart2()

# API for generative AI response
@app.route('/api/generative_ai_response/chart1', methods=['POST'])
def ai_response_chart1():
    return filter_data.ai_response_chart1()
@app.route('/api/generative_ai_response/chart2', methods=['POST'])
def ai_response_chart2():
    return filter_data.ai_response_chart2()


# API for chatbot
@app.route('/api/chat-bot', methods=['POST'])
def chatbot_response():
    return chatbot.chatbot_response()



if __name__ == '__main__':
    
    # Update cloud every 1 second
    cloud.start_update_thread()
    
    app.run(debug=True, use_reloader=False)
