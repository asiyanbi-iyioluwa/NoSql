# web_app.py
from flask import Flask, request, render_template, jsonify
import requests
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

WAF_URL = "http://127.0.0.1:5001/filter_query"
DETECTION_API_URL = "http://127.0.0.1:5002/detect"

@app.route("/home", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Simulated query (vulnerable)
        sql_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Generated SQL Query: {sql_query}")

        # Step 1: WAF
        waf_response = requests.post(WAF_URL, json={"query": sql_query})
        if waf_response.status_code != 200 or "error" in waf_response.json():
            return jsonify({"error": "Blocked by WAF: Possible SQL Injection detected!"})

        # Step 2: ML Detection
        detection_response = requests.post(DETECTION_API_URL, json={"query": sql_query})
        result = detection_response.json()
        if result["prediction"] == "SQL Injection Detected":
            return jsonify({"error": "SQL Injection Detected!"})

        return jsonify({"message": "Login successful!"})
    return render_template("login.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

def send_alert_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "admin_email@gmail.com"
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("your_email@gmail.com", "your_app_password")
        smtp.send_message(msg)

send_alert_email("SQLi Detected!", f"Query: {query}")

import logging

logging.basicConfig(
    filename="sqli_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Example
logging.info(f"Safe login attempt: {query}")
logging.warning(f"Blocked by WAF: {query}")
logging.error(f"ML detected SQLi: {query}")
