from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/")
def home():
    return "It works!"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    email_body_raw = data.get("email_body", "") if data else ""

    if not email_body_raw:
        return jsonify({"error": "No email body provided"}), 400

    # Convert raw HTML email body to plain text
    soup = BeautifulSoup(email_body_raw, "html.parser")
    email_body_text = soup.get_text(separator="\n", strip=True)

    try:
        response = model.generate_content(f"Summarize this email:\n{email_body_text}")
        summary = response.text

        # Send summary to Discord
        if DISCORD_WEBHOOK_URL:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": f"📧 **Email Summary**:\n{summary}"})

        return jsonify({"summary": response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
