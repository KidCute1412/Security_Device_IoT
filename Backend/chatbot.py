import json
from urllib import response
from Backend.gemini_api import model
from flask import request, jsonify
import re
from datetime import date, timedelta
type_question = ["daily_summary", "lastest_alert", "compare_days", "device_info", "unknown"]



def today():
    return date.today().strftime("%Y-%m-%d")

def handle_question_type(type):
    if type == "daily_summary":
        return "Tóm tắt ngày hôm nay"
    elif type == "lastest_alert":
        return "Cảnh báo mới nhất"
    elif type == "compare_days":
        return "So sánh các ngày"
    elif type == "device_info":
        return "Thông tin thiết bị"
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
        Trả lời câu hỏi của người dùng theo dạng JSON với các trường "type" (loại câu hỏi), "days" (danh sách các ngày) và "devices" (danh sách các thiết bị)
        (Kết quả trả về đúng định dạng chuẩn json không thêm bớt gì thêm, không trả về title của prompt hay gì cả).
        Nếu dữ liệu ngày tháng năm không đầy đủ, ví dụ thiếu năm thì hãy mặc định là năm hiện tại, nếu thiếu tháng thì hãy mặc định là tháng hiện tại.
        Nếu thiếu ngày thì hãy mặc định là ngày đầu tiên của tháng hiện tại.
        Các thiết bị chỉ bao gồm: cảm biến rung, cảm biến chuyển động pir, đèn led, buzzer, màn hình lcd.
        Dữ liệu ngày tháng có định dạng "YYYY-MM-DD" (Biết rằng hôm nay là {today()}).
        """
        chat_response = model.generate_content(prompt) # This is a string has JSON format
        
        response = chat_response.text.strip()
        clean_text = re.sub(r"```json|```", "", response).strip()
        try:
            response_data = json.loads(clean_text)
            type = response_data.get("type", "unknown")
            list_days = response_data.get("days", [])
            list_devices = response_data.get("devices", [])
        except json.JSONDecodeError:
            return jsonify({"status": "ERROR", "message": "Invalid JSON format in model response"}), 500
        
        print (f"Received question type: {type}, days: {list_days}, devices: {list_devices}")
        
        response = clean_text
        return jsonify({
            "status": "OKE",
            "message": "Chatbot response successful",
            "response": response
        }), 200
    else:
        return jsonify({"status": "ERROR", "message": "Method not allowed"}), 405
    




