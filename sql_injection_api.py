from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from waitress import serve

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Load the trained model and TF-IDF vectorizer
tfidf_vectorizer = joblib.load("tfidf_vectorizer_OS.pkl")
model = joblib.load("trained_model_OS.pkl")

@app.route('/', methods=['POST'])
def detect_OS_injection_api():
    username = request.json.get('username')
    password = request.json.get('password')

    # If no SQL injection patterns are found, use the trained model
    query = tfidf_vectorizer.transform([username, password ])
    predictions = model.predict(query)

    return jsonify({
        "username_is_OS_Command_injection": bool(predictions[0]),
        "password_is_OS_Command_injection": bool(predictions[1]),
        #"message": "SQL injection detection results"
    })

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5009)
