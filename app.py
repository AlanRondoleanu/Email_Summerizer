from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

api_key = "AIzaSyCpinojIutp_G0LLPLRfWDlyA88hAyOYOA"
genai.configure(api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash")

@app.route("/")
def home():
    return "It works!"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    email = data.get("email_body", "")
    
    if not email:
        return jsonify({"error": "No email body provided"}), 400

    try:
        response = model.generate_content(f"Summarize this email:\n{email}")
        return jsonify({"summary": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
