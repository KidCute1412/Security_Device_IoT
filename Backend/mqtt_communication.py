import paho.mqtt.client as mqtt
import Backend.global_vars as glb
import json
from flask import request, jsonify





# 3MSSV/username/received_data [pir_sensor, vibration_sensor, led, buzzer, lcd]
# 3MSSV/username/control_data [led, buzzer, lcd]
# 3MSSV/unification [username]




def on_message(client, userdata, msg):
    """
    Callback function to handle incoming MQTT messages.
    This is called automatically when loop_start() is running and messages arrive.
    """
    try:
        json_data = json.loads(msg.payload.decode())
        print(f"[MQTT] Received message on topic {msg.topic}: {json_data}")
        
        # Process the received sensor data
        if msg.topic.endswith("received_data"):
            process_received_data(json_data)  # Process the incoming sensor data
        
    except json.JSONDecodeError as e:
        print(f"[MQTT] JSON decode error: {e}")
    except Exception as e:
        print(f"[MQTT] Error processing message: {e}")

    
# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message  # Fixed: removed () - should be function reference, not function call
mqtt_client.connect("broker.hivemq.com", 1883, 60)


### # 3MSSV/unification [username]

def unification(username=None):

    # Create JSON payload
    payload_data = {
        "username": username or glb.global_username if hasattr(glb, 'global_username') else "unknown"
    }
    
    # Convert to JSON string
    json_payload = json.dumps(payload_data)
    
    try:
        # Publish JSON data
        result = mqtt_client.publish(f"/23127061_23127158_23127404/unification", json_payload)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] Unification message sent successfully: {json_payload}")
            glb.global_successfully_connected = True  # Set the flag to indicate successful connection
            return True
        else:
            print(f"[MQTT] Failed to send unification message. Error code: {result.rc}")
            return False
            
    except Exception as e:
        print(f"[MQTT] Error sending unification message: {e}")
        return False



# 3MSSV/username/received_data [pir_sensor, vibration_sensor, led, buzzer, lcd]
def setup_mqtt_subscription():
    """
    Subscribe to sensor data topic and start listening.
    This should be called once during initialization.
    """
    try:
        if hasattr(glb, 'global_username') and glb.global_username:
            topic = f"/23127061_23127158_23127404/{glb.global_username}/received_data"
            mqtt_client.subscribe(topic)
            mqtt_client.loop_start()  # Start the MQTT client loop to process incoming messages
            print(f"[MQTT] Subscribed to sensor data topic: {topic}")
            return True
        else:
            print("[MQTT] Cannot subscribe: global_username not set")
            return False
    except Exception as e:
        print(f"[MQTT] Error subscribing to sensor data: {e}")
        return False



def process_received_data(json_data):
    """
    Process incoming sensor data (called from on_message).
    """
    try:
        # Update global variables with received sensor data
        # INPUT DEVICES
        if "pir_sensor" in json_data:
            glb.current_pir_sensor = json_data["pir_sensor"]
        if "vibration_sensor" in json_data:
            glb.current_vibration_sensor = json_data["vibration_sensor"]
        
        # OUPUT DEVICES
        if "led" in json_data:
            glb.current_led_status = json_data["led"]
        if "buzzer" in json_data:
            glb.current_buzzer_status = json_data["buzzer"]
        if "lcd" in json_data:
            glb.current_lcd_status = json_data["lcd"]
        
        print(f"[SENSOR] Updated - PIR: {glb.current_pir_sensor}, Vibration: {glb.current_vibration_sensor}")
        
    except Exception as e:
        print(f"[MQTT] Error processing sensor data: {e}")

    

# 3MSSV/username/control_data [led, buzzer, lcd]

def command_to_devices():
    data = request.get_json()
    if not data:
        return jsonify({"status": "ERROR", "message": "No data provided"}), 400
    
    glb.current_led_status = data.get("led_status", glb.current_led_status)
    glb.current_buzzer_status = data.get("buzzer_status", glb.current_buzzer_status)
    glb.current_lcd_status = data.get("lcd_status", glb.current_lcd_status)

    commands = {
        "led_status": glb.current_led_status,
        "buzzer_status": glb.current_buzzer_status,
        "lcd_status": glb.current_lcd_status
    }
    try:
        # Publish commands to MQTT
        send_control_data(commands)
        
        return jsonify({
            "status": "OKE",
            "message": "Commands sent successfully",
            "commands": commands
        })
    except Exception as e:
        print(f"[MQTT] Error sending control data: {e}")
        return jsonify({
            "status": "ERROR",
            "message": f"Error sending control data: {str(e)}"
        }), 500

def send_control_data(commands):
    """
    Send control commands to ESP32 device
    
    Args:
        commands (dict): Dictionary with device commands
                        Example: {"led": 1, "buzzer": 0, "lcd": 1}
    """

    
    # Handle both dictionary and list formats
    if isinstance(commands, dict):
        # Dictionary format: {"led": 1, "buzzer": 0, "lcd": 1}
        payload_data = {
            "commands": commands
        }
    else:
        print(f"[MQTT] Invalid commands format: {type(commands)}")
        return False
    
    json_payload = json.dumps(payload_data)
    topic = f"/23127061_23127158_23127404/{glb.global_username}/control_data"
    try:
        result = mqtt_client.publish(topic, json_payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] Control data sent: {json_payload}")
            return True
        else:
            print(f"[MQTT] Failed to send control data. Error code: {result.rc}")
            return False
    except Exception as e:
        print(f"[MQTT] Error sending control data: {e}")
        return False
    
