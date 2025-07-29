from flask import request, jsonify, Response
import google.generativeai as genai
import os
import json
from requests import get
from Backend.cloud_database import user_account_collection

demo_user_name = "admin"
def get_demo_user_info():
    user = user_account_collection.find_one({"username": demo_user_name})
    if user:
        return {
            "username": user["username"],
            "phone_number": user["phonenumber"],
            "password": user["password"]
        }
    else:
        return None



# Configure the Google Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyC_8QmevewXuFJBQsr3KV6qeS7LnWj6RUA"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash-001")



def analyze_password_strength():
    data = get_demo_user_info()
    password  = data["password"] if data else "default_password"
    print(f"Received password for analysis: {password}")

    prompt = f"""
    Dưới đây là một mật khẩu: "{password}".
    Hãy phân tích mật khẩu này và đánh giá độ mạnh của nó một cách ngắn gọn (dưới 20 từ). Trả lời bằng tiếng Việt.
    """
    response = model.generate_content(prompt)
    analysis = response.text.strip()
    return Response(
        json.dumps({
            "status": "OKE",
            "message": "Password analysis successful",
            "analysis": analysis
        }, ensure_ascii=False),
        mimetype='application/json'
    )