import json
from tracemalloc import start

from click import prompt
from Backend.gemini_api import model
from flask import request, jsonify
import re
from datetime import date, datetime
from Backend.cloud_database import sensor_data_collection, alert_collection
import Backend.global_vars as gv

type_question = ["alert_statistic", "lastest_alert", "compare_days", "sensor_device_info", "unknown",
                 "realtime_status"]

# Alert_history: lần báo động, số pir, vibaration trong 1 ngày cụ thể (cần 1 day và ko cảm biến)
# Nếu có thêm tên cảm biến thì chỉ trả về cảm biến đó

# Lastest_alert: Trả về cảnh báo mới nhất (cần 1 day và ko cảm biến) (mặc định ngày hôm nay)

# Compare_days: So sánh các ngày (cần 2 days và ko cảm biến), nếu có tên cảm biến thì chỉ so sánh cảm biến đó

# Device_info: Trả về thông tin thiết bị (cần 1 device và ko ngày tháng)

# Realtime_status: Trả về trạng thái hiện tại của thiết bị (cần 1 device và ko ngày tháng)

def handle_alert_statistic(list_days, list_devices):
    if len(list_days) == 0:
        return "Dữ liệu ngày tháng không đầy đủ, vui lòng cung cấp ít nhất một ngày."
    if len(list_days) > 1:
        return "Chỉ hỗ trợ một ngày cho lịch sử cảnh báo."
    
    # Truy xuất dữ liệu cảnh báo từ cơ sở dữ liệu và trả về kiểu chuỗi
    alert_text, pir_sensor_text, vibration_sensor_text = "", "", ""
    day = list_days[0]
    start_date = datetime.strptime(day, "%Y-%m-%d")
    end_date = start_date.replace(hour=23, minute=59, second=59)
    alerts = alert_collection.find({"user_id": gv.global_id, 
                                    "timestamp": {"$gte": start_date, 
                                                  "$lt": end_date}})
    if not alerts:
        alert_text = "Không có cảnh báo nào trong ngày này."
    else:
        alert_text = f"Có {alerts.count()} cảnh báo trong ngày {day}."

    if len(list_devices) == 0:
        return alert_text
    
    # print("Start:", start_date)
    # print("End:", end_date)

    # doc = sensor_data_collection.find_one({"sensor_type": "pir"})
    # print("Timestamp in doc:", doc)
    if "pir" in list_devices:
        print (gv.global_id)
        pir_sensors = sensor_data_collection.find({"user_id": gv.global_id,
                                                    "sensor_type": "pir_sensor", 
                                                   "timestamp": {"$gte": start_date, 
                                                                 "$lt": end_date}})
        if not pir_sensors:
            pir_sensor_text = "Không có dữ liệu cảm biến chuyển động PIR trong ngày này."
        else:
            pir_sensor_text = f"Có {pir_sensors.count()} dữ liệu cảm biến chuyển động PIR trong ngày {day}."
    if "vibration" in list_devices:
        vibration_sensors = sensor_data_collection.find({"user_id": gv.global_id, "sensor_type": "vibration_sensor", 
                                                        "timestamp": {"$gte": start_date, 
                                                                      "$lt": end_date}})
        
        if not vibration_sensors:
            vibration_sensor_text = "Không có dữ liệu cảm biến rung trong ngày này."
        else:
            vibration_sensor_text = f"Có {vibration_sensors.count()} dữ liệu cảm biến rung trong ngày {day}."
    return f"{alert_text}\n{pir_sensor_text}\n{vibration_sensor_text}".strip()


def handle_lastest_alert(list_days, list_devices):
    if len(list_days) == 0:
        list_days.append(today())
    if len(list_days) > 1:
        return "Chỉ hỗ trợ một ngày cho cảnh báo mới nhất."
    
    day = list_days[0]
    start_date = datetime.strptime(day, "%Y-%m-%d")
    end_date = start_date.replace(hour=23, minute=59, second=59)
    latest_alert = alert_collection.find_one({"user_id": gv.global_id, 
                                              "timestamp": {"$gte": start_date, 
                                                            "$lt": end_date}},
                                             sort=[("timestamp", -1)])
    alert_text = ""
    if not latest_alert:
        alert_text = "Không có cảnh báo mới nhất trong ngày này."
    
    else:
        alert_text = f"Cảnh báo mới nhất trong ngày {day}: {latest_alert['timestamp']}"
    
    if len(list_devices) == 0:
        return alert_text
    
    if "pir" in list_devices:
        pir_sensor = sensor_data_collection.find_one({"user_id": gv.global_id, "sensor_type": "pir", 
                                                      "timestamp": {"$gte": start_date, 
                                                                    "$lt": end_date}},
                                                     sort=[("timestamp", -1)])
        if pir_sensor:
            alert_text += f"\nCảm biến chuyển động PIR mới nhất: {pir_sensor['timestamp']}"
    
    if "vibration" in list_devices:
        vibration_sensor = sensor_data_collection.find_one({"user_id": gv.global_id, "sensor_type": "vibration", 
                                                            "timestamp": {"$gte": start_date, 
                                                                          "$lt": end_date}},
                                                           sort=[("timestamp", -1)])
        if vibration_sensor:
            alert_text += f"\nCảm biến rung mới nhất: {vibration_sensor['timestamp']}"
    
    return alert_text

def handle_compare_days(list_days, list_devices):
    if len(list_days) != 2:
        return "Chỉ hỗ trợ so sánh hai ngày."
    
    day1, day2 = list_days
    if day1 == day2:
        return "Hai ngày không được giống nhau."
    start_date1 = datetime.strptime(day1, "%Y-%m-%d")
    end_date1 = start_date1.replace(hour=23, minute=59, second=59)
    start_date2 = datetime.strptime(day2, "%Y-%m-%d")
    end_date2 = start_date2.replace(hour=23, minute=59, second=59)
    alert_day1 = alert_collection.find({"user_id": gv.global_id, 
                                        "timestamp": {"$gte": start_date1, 
                                                      "$lt": end_date1}})
    alert_day2 = alert_collection.find({"user_id": gv.global_id, 
                                        "timestamp": {"$gte": start_date2, 
                                                      "$lt": end_date2}})
    
    alert_text = f"Có {alert_day1.count()} cảnh báo trong ngày {day1} và {alert_day2.count()} cảnh báo trong ngày {day2}."
    
    if len(list_devices) == 0:
        return alert_text
    
    if "pir" in list_devices:
        pir_sensors_day1 = sensor_data_collection.find({"user_id": gv.global_id, "sensor_type": "pir", 
                                                        "timestamp": {"$gte": start_date1, 
                                                                      "$lt": end_date1}})
        pir_sensors_day2 = sensor_data_collection.find({"user_id": gv.global_id, "sensor_type": "pir", 
                                                        "timestamp": {"$gte": start_date2, 
                                                                      "$lt": end_date2}})
        pir_sensor_text = (f"Có {pir_sensors_day1.count()} dữ liệu cảm biến chuyển động PIR trong ngày {day1} "
                           f"và {pir_sensors_day2.count()} dữ liệu cảm biến chuyển động PIR trong ngày {day2}.")
        alert_text += "\n" + pir_sensor_text
    
    if "vibration" in list_devices:
        vibration_sensors_day1 = sensor_data_collection.find({"user_id": gv.global_id, "sensor_type": "vibration", 
                                                              "timestamp": {"$gte": start_date1, 
                                                                            "$lt": end_date1}})
        vibration_sensors_day2 = sensor_data_collection.find({"user_id": gv.global_id, "sensor_type": "vibration", 
                                                              "timestamp": {"$gte": start_date2, 
                                                                            "$lt": end_date2}})
        vibration_sensor_text = (f"Có {vibration_sensors_day1.count()} dữ liệu cảm biến rung trong ngày {day1} "
                                 f"và {vibration_sensors_day2.count()} dữ liệu cảm biến rung trong ngày {day2}.")
        alert_text += "\n" + vibration_sensor_text
    return alert_text

def handle_device_info(list_devices):
    # Call gemini model to get device info
    if len(list_devices) == 0:
        return "Vui lòng cung cấp ít nhất một thiết bị."
    if (len(list_devices) > 3):
        return "Quá nhiều thiết bị, vui lòng cung cấp tối đa 3 thiết bị."
    device_info = ""
    prompt = f"""Dưới đây là danh sách các thiết bị: {', '.join(list_devices)}.
    Trả lời thôm tin về các thiết bị này (chức năng, nguyên lý hoạt động, cách sử dụng, v.v.), giới hạn số từ cho mỗi thiết bị là 30 từ."""
    response = model.generate_content(prompt)
    device_info = response.text.strip()
    return device_info

def handle_realtime_status(list_devices):
    if len(list_devices) == 0:
        return "Vui lòng cung cấp ít nhất một thiết bị."
    status_text = ""
    for device in list_devices:
        if device == "pir":
            result = "Phát hiện chuyển động" if gv.current_pir_sensor else "Không phát hiện chuyển động"
            status_text += f"Cảm biến chuyển động PIR hiện tại: {result}\n"
        elif device == "vibration":
            result = "Phát hiện rung" if gv.current_vibration_sensor else "Không phát hiện rung"
            status_text += f"Cảm biến rung hiện tại: {result}\n"
        elif device == "led":
            result = "Bật" if gv.current_led_status else "Tắt"
            status_text += f"Trạng thái đèn LED hiện tại: {result}\n"
        elif device == "buzzer":
            result = "Bật" if gv.current_buzzer_status else "Tắt"
            status_text += f"Trạng thái buzzer hiện tại: {result}\n"
        elif device == "lcd":
            result = "Chống trộm" if gv.current_lcd_status == 1 else "Thông tin"
            status_text += f"Trạng thái màn hình LCD hiện tại: {result}\n"
    return status_text.strip()        

def today():
    return date.today().strftime("%Y-%m-%d")

def handle_question_type(type, list_days, list_devices):
    if type == "alert_statistic":
        #simulate:
        # return f"Đây là lịch sử cảnh báo trong ngày {list_days[0]} cho các thiết bị {', '.join(list_devices)}"
        return handle_alert_statistic(list_days, list_devices)
    elif type == "lastest_alert":
        # simulate:
        if len(list_days) == 0:
            list_days.append(today())
        # return f"Đây là cảnh báo mới nhất trong ngày {list_days[0]} cho các thiết bị {', '.join(list_devices)}"
        return handle_lastest_alert(list_days, list_devices)
    elif type == "compare_days":
        # simulate:
        # return f"Đây là so sánh giữa ngày {list_days[0]} và {list_days[1]} cho các thiết bị {', '.join(list_devices)}"
        return handle_compare_days(list_days, list_devices)
    elif type == "sensor_device_info":
        # simulate:
        # return f"Đây là thông tin về các thiết bị {', '.join(list_devices)}"
        return handle_device_info(list_devices)
    elif type == "realtime_status":
        # simulate:
        # return f"Đây là trạng thái hiện tại của các thiết bị {', '.join(list_devices)}"
        return handle_realtime_status(list_devices)
    else:
        return "Không rõ loại câu hỏi"

def chatbot_response():
    if request.method == "POST":
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"status": "ERROR", "message": "No message provided"}), 400
        # Some variables to query the database 
        list_days = []
        list_devices = []
        type = "unknown"


        # Generate a response using the Gemini model

        prompt = f"""Phân loại câu hỏi của người dùng thành các loại sau: {', '.join(type_question)}
        Dưới đây là câu hỏi của người dùng: {user_message}.
        Định dạng trả về JSON:
        {{
            "type": loại câu hỏi,
            "days": danh sách các ngày (dạng "YYYY-MM-DD"),
            "devices": danh sách các thiết bị (["pir", "vibration", "led", "buzzer", "lcd"] (Chỉ hiển thị những giá trị trong danh sách này))
        }}
        Nếu dữ liệu ngày tháng năm không đầy đủ, ví dụ thiếu năm thì hãy mặc định là năm hiện tại, nếu thiếu tháng thì hãy mặc định là tháng hiện tại.
        Nếu thiếu ngày thì hãy mặc định là ngày đầu tiên của tháng hiện tại.
        (Biết rằng hôm nay là {today()}).
        """
        chat_response = model.generate_content(prompt) # This is a string has JSON format
        
        response = chat_response.text.strip()
        clean_text = re.sub(r"```json|```", "", response).strip()
        print(clean_text)
        try:
            response_data = json.loads(clean_text)
            type = response_data.get("type", "unknown")
            list_days = response_data.get("days", [])
            list_devices = response_data.get("devices", [])
        except json.JSONDecodeError:
            return jsonify({"status": "ERROR", "message": "Invalid JSON format in model response"}), 500
        
        print (f"Received question type: {type}, days: {list_days}, devices: {list_devices}")
        
        response = handle_question_type(type, list_days, list_devices)
        return jsonify({
            "status": "OKE",
            "message": "Chatbot response successful",
            "response": response
        }), 200
    else:
        return jsonify({"status": "ERROR", "message": "Method not allowed"}), 405
    




