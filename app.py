from flask import Flask, redirect, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
import random
import Backend.account as account
import Backend.gemini_api as gemini_api
import Backend.filter_data as filter_data
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



if __name__ == '__main__':
   app.run(debug = True)