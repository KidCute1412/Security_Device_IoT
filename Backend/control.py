import Backend.global_vars as glb
import json
import Backend.mqtt_communication as mqtt
from flask import request, jsonify  







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
        mqtt.send_control_data(commands)
        
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