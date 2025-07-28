from flask import Flask, redirect, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
import random
import Backend.account as account

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


if __name__ == '__main__':
   app.run(debug = True)