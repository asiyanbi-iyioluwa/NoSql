# detection_api.py
from flask import Flask, request, jsonify
import joblib
import re

app = Flask(__name__)

# Load trained model
model = joblib.load("sqli_detector_model.pkl")

@app.route("/detect", methods=["POST"])
def detect_sqli():
    data = request.get_json()
    query = data.get("query", "")

    # Preprocess the query as you did during training
    processed_query = preprocess(query)
    features = vectorizer.transform([processed_query])

    prediction = model.predict(features)[0]

    if prediction == 1:
        return jsonify({"prediction": "SQL Injection Detected"})
    else:
        return jsonify({"prediction": "Query is safe"})

def preprocess(query):
    # Basic preprocessing (should match your training pipeline)
    return re.sub(r"[^\w\s]", "", query.lower())


# @app.route("/detect", methods=["POST"])
# def detect():
#     data = request.get_json()
#     query = data["query"]

#     # Dummy logic: if query contains ' OR ' it’s a SQLi
#     if " OR " in query.upper():
#         return jsonify({"prediction": "SQL Injection Detected"})
#     return jsonify({"prediction": "Clean"})

if __name__ == "__main__":
    app.run(port=5002)
