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

@app.route('/check-note', methods=['POST'])
def check_note():
    note = request.json.get('note')

    # Vectorize input for XSS detection
    input_vectorized = tfidf_vectorizer.transform([note]).toarray()

    # Predict XSS for the note
    prediction_OS = model.predict(input_vectorized)

    response = {
        "is_OS_command_injection": bool(prediction_OS),
    }

    if response["is_OS_command_injection"]:
        response["message"] = "OS Command injection detected"
    else:
        response["message"] = "OS Command injection not detected"


    return jsonify(response)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5009)
