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
def detect_sql_injection_api():
    username = request.json.get('username')
    password = request.json.get('password')

    # Regular expression for detecting SQL injection patterns
    #sql_pattern = re.compile(r".*(\'|\"|;|--|union|truncate|-).*")

    # Check for SQL injection patterns in the username and password
    #username_is_sql_injection = bool(sql_pattern.match(username))
    #password_is_sql_injection = bool(sql_pattern.match(password))

    # If SQL injection is detected, return appropriate response
    #if username_is_sql_injection or password_is_sql_injection:
    #    return jsonify({
    #        "username_is_sql_injection": username_is_sql_injection,
    #        "password_is_sql_injection": password_is_sql_injection,
    #        "message": "SQL injection detected"
    #    })

    # If no SQL injection patterns are found, use the trained model
    query = tfidf_vectorizer.transform([username.lower(), password.lower()])
    predictions = model.predict(query)

    return jsonify({
        "username_is_OS_Command_injection": bool(predictions[0]),
        "password_is_OS_Command_injection": bool(predictions[1]),
        #"message": "SQL injection detection results"
    })

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5009)
