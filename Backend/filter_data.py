from flask import  request, jsonify
from Backend.gemini_api import model

start_date_chart1 = None
end_date_chart1 = None
date_chart2 = None

# GET date filter for chart 1
def get_date_chart1():
    global start_date_chart1, end_date_chart1
    if request.method == "POST":
        data = request.get_json()
        start_date_chart1 = data.get("start_date")
        end_date_chart1 = data.get("end_date")
        print(f"Received date range for chart 1: {start_date_chart1} to {end_date_chart1}")
        return jsonify({"status": "OKE", "message": "Date range for chart 1 set successfully"}), 200
    else:
        return jsonify({"status": "ERROR", "message": "Method not allowed"}), 405
    
# GET date filter for chart 2
def get_date_chart2():
    global date_chart2
    if request.method == "POST":
        data = request.get_json()
        date_chart2 = data.get("date")
        print(f"Received date for chart 2: {date_chart2}")
        return jsonify({"status": "OKE", "message": "Date for chart 2 set successfully"}), 200
    else:
        return jsonify({"status": "ERROR", "message": "Method not allowed"}), 405
    


# Generative AI response for chart 1
def ai_response_chart1():
    start_date = start_date_chart1
    end_date = end_date_chart1
    prompt = f"""    Dưới đây là khoảng thời gian: từ {start_date} đến {end_date}. 
    Tạm thời bạn hãy in ra khoảng thời gian này và kiểu chào buổi sáng vui vẻ, tầm 30 từ."""
    response = model.generate_content(prompt)
    analysis = response.text.strip()
    return jsonify({
        "status": "OKE",
        "message": "Generative AI response for chart 1 successful",
        "analysis": analysis
    }), 200

# Generative AI response for chart 2
def ai_response_chart2():
    date = date_chart2
    prompt = f"""    Dưới đây là ngày: {date}. 
    Tạm thời bạn hãy in ra ngày này và kiểu chào buổi sáng vui vẻ, tầm 30 từ."""
    response = model.generate_content(prompt)
    analysis = response.text.strip()
    return jsonify({
        "status": "OKE",
        "message": "Generative AI response for chart 2 successful",
        "analysis": analysis
    }), 200
