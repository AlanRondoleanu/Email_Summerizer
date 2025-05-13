from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return "It works!"


@app.route("/summarize", methods=["GET"])
def test_get():
    return "GET request to /summarize received!"

@app.route("/summarize", methods=["POST"])
def test_post():
    data = request.get_json()
    return jsonify({
        "message": "POST request to /summarize received!",
        "data_received": data
    })

if __name__ == "__main__":
    app.run()
