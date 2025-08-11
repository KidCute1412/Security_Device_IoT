from flask import  request, jsonify
from Backend.gemini_api import model
from datetime import datetime, timedelta
from Backend.cloud_database import alert_collection
import Backend.global_vars as gv

start_date_chart1 = None
end_date_chart1 = None
date_chart2 = None

def get_alerts_per_day():
    try:
        global start_date_chart1, end_date_chart1
        # Nếu chưa có giá trị, lấy mặc định 7 ngày gần nhất
        if not start_date_chart1 or not end_date_chart1:
            today = datetime.now()
            start = today - timedelta(days=7)
            end = today
            start_date_chart1 = start.strftime("%Y-%m-%d")
            end_date_chart1 = end.strftime("%Y-%m-%d")
        else:
            start = datetime.strptime(start_date_chart1, "%Y-%m-%d")
            end = datetime.strptime(end_date_chart1, "%Y-%m-%d")
        end = end + timedelta(days=1)
        alerts = alert_collection.find({
            "user_id": gv.global_id,
            "timestamp": {"$gte": start, "$lt": end}
        })
        # Count per day
        day_counts = {}
        for alert in alerts:
            day = alert["timestamp"].strftime("%Y-%m-%d")
            day_counts[day] = day_counts.get(day, 0) + 1
        # Fill missing days with 0
        days = []
        counts = []
        cur = start
        while cur < end:
            day_str = cur.strftime("%Y-%m-%d")
            days.append(day_str)
            counts.append(day_counts.get(day_str, 0))
            cur += timedelta(days=1)
        return jsonify({"status": "OKE", "labels": days, "data": counts}), 200
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500


def get_alerts_per_hour():
    try:
        global date_chart2
        if not date_chart2:
            # Default to today if not set
            date_chart2 = datetime.now().strftime("%Y-%m-%d")
        date_obj = datetime.strptime(date_chart2, "%Y-%m-%d")
        start = date_obj
        end = date_obj + timedelta(days=1)
        alerts = alert_collection.find({
            "user_id": gv.global_id,
            "timestamp": {"$gte": start, "$lt": end}
        })
        # Count per hour
        hour_counts = {}
        for alert in alerts:
            hour = alert["timestamp"].hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        # Fill missing hours with 0
        hours = [f"{h}h" for h in range(24)]
        counts = [hour_counts.get(h, 0) for h in range(24)]
        return jsonify({"status": "OKE", "labels": hours, "data": counts}), 200
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
    

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
    data_message = request.get_json()
    labels, data = data_message.get("labels"), data_message.get("data")
    start_date = start_date_chart1
    end_date = end_date_chart1
    prompt = f"""    Dưới đây là khoảng thời gian: từ {start_date} đến {end_date}. 
    Đây là dữ liệu các ngày: {labels} và dữ liệu tương ứng: {data}.
    Nếu dữ liệu các ngày không có thì trả về "Không có dữ liệu".
    Nếu dữ liệu các ngày có thì hãy phân tích và đưa ra nhận xét, xu hướng của dữ liệu này. 
    Biết đây là dữ liệu số báo động chống trộm trong các ngày tương ứng.
    Trả lời khoảng 200 từ. (tất cả là text tiếng Việt)
    """
    response = model.generate_content(prompt)
    analysis = response.text.strip()
    return jsonify({
        "status": "OKE",
        "message": "Generative AI response for chart 1 successful",
        "analysis": analysis
    }), 200

# Generative AI response for chart 2
def ai_response_chart2():
    data_message = request.get_json()
    labels, data = data_message.get("labels"), data_message.get("data")
    date = date_chart2
    prompt = f"""    Dưới đây là ngày: {date}. 
    Đây là dữ liệu giờ trong ngày: {labels} và dữ liệu tương ứng: {data}.
    Nếu dữ liệu giờ không có thì trả về "Không có dữ liệu".
    Nếu dữ liệu giờ có thì hãy phân tích và đưa ra nhận xét, xu hướng của dữ liệu này. 
    Biết đây là dữ liệu số báo động chống trộm theo các giờ trong ngày đang xét.
    Trả lời khoảng 200 từ.(tất cả là text tiếng Việt)"""
    response = model.generate_content(prompt)
    analysis = response.text.strip()
    return jsonify({
        "status": "OKE",
        "message": "Generative AI response for chart 2 successful",
        "analysis": analysis
    }), 200
