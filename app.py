from flask import Flask, redirect, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
import random
import Backend.account as account
import paho.mqtt.client as mqtt
import Backend.mqtt_communication as mqtt
import Backend.control as control
# Biến toàn cục lưu dữ liệu sensor
mqtt_data = {
    "reed_sensor": False,
    "pir_sensor": False,
    "vibration_sensor": False
}



    


import Backend.gemini_api as gemini_api
import Backend.filter_data as filter_data
import Backend.chatbot as chatbot
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Bonus function
def simulate_sensor():
   # Simulate sensor data
   reed_sensor = random.choice([True, False])
   pir_sensor = random.choice([True, False])
   vibration_sensor = random.choice([True, False])

   return reed_sensor, pir_sensor, vibration_sensor
# Initial page
@app.route('/')
def first_page():
   return redirect("/Frontend/HTML/login.html")
@app.route('/Frontend/<path:filename>')
def serve_frontend(filename):
    return send_from_directory('Frontend', filename)



# API for getting current sensor data (page HOME)
@app.route('/api/sensor_status', methods=['GET'])

def get_status():
   reed_sensor, pir_sensor, vibration_sensor = simulate_sensor()
   return jsonify({"status": "OKE", "message": "Server is running",
                   "reed_sensor": reed_sensor,
                   "pir_sensor": pir_sensor,
                   "vibration_sensor": vibration_sensor})

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
    return control.command_to_devices()

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
    
    # Initialize MQTT client
    


    app.run(debug=True, use_reloader=False) 
    
