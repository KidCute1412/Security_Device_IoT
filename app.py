from flask import Flask, redirect, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
import random
import Backend.account as account
import paho.mqtt.client as mqtt


# Biến toàn cục lưu dữ liệu sensor
mqtt_data = {
    "reed_sensor": False,
    "pir_sensor": False,
    "vibration_sensor": False
}

def on_message(client, userdata, msg):
    print(f"[DEBUG] Callback from client id: {id(client)}")
    topic = msg.topic
    payload = msg.payload.decode()
    
    print(f"[MQTT] Topic: {topic}, Payload: {payload}") 

    

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
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
    from Backend.cloud_database import sensor_data_collection
    from Backend.global_vars import global_id
    import datetime
    reed_sensor, pir_sensor, vibration_sensor = simulate_sensor()
    # Save to cloud if any sensor is True
    now = datetime.datetime.utcnow()
    user_id = global_id
    if reed_sensor:
        sensor_data_collection.insert_one({
            "user_id": user_id,
            "sensor_type": "reed_sensor",
            "timestamp": now
        })
    if pir_sensor:
        sensor_data_collection.insert_one({
            "user_id": user_id,
            "sensor_type": "pir_sensor",
            "timestamp": now
        })
    if vibration_sensor:
        sensor_data_collection.insert_one({
            "user_id": user_id,
            "sensor_type": "vibration_sensor",
            "timestamp": now
        })
    return jsonify({"status": "OKE", "message": "Server is running",
                    "reed_sensor": reed_sensor,
                    "pir_sensor": pir_sensor,
                    "vibration_sensor": vibration_sensor})

# API for login
@app.route('/api/login', methods=['POST'])
def login_process():
   return account.login()


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
    # Chỉ chạy MQTT client ở process chính
    mqtt_client.connect("broker.hivemq.com", 1883, 60)
    mqtt_client.subscribe("/data/pir_sensor")
    mqtt_client.loop_start()
    app.run(debug=True, use_reloader=False)