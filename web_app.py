from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os
# Load the trained model and vectorizer
model_lr = joblib.load('logistic_regression_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')

# Custom threshold
POSITIVE_THRESHOLD = 0.65
NEGATIVE_THRESHOLD = 0.58

# Initialize Flask app
app = Flask(__name__)

def predict_sentiment(review_text):
    # Vectorize the review
    vectorized = tfidf_vectorizer.transform([review_text])

    # Get probability for class 'positive' (index 1)
    prob_positive = model_lr.predict_proba(vectorized)[0][1]

    # Apply thresholds to classify sentiment
    if prob_positive >= POSITIVE_THRESHOLD:
        sentiment = "Positive 😊"
    elif prob_positive <= NEGATIVE_THRESHOLD:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"  # Neutral range between 0.45 and 0.65

    confidence = round(prob_positive, 4)

    return sentiment, confidence

# Home route (optional if using HTML form)
@app.route('/')
def home():
    return render_template('dashboard.html')  # Make sure index.html exists in a 'templates' folder

# API route for POST requests
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'review' not in data:
        return jsonify({'error': 'Missing review text'}), 400

    review_text = data['review']
    sentiment, confidence = predict_sentiment(review_text)

    return jsonify({
        'review': review_text,
        'sentiment': sentiment,
        'confidence': confidence
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from env on Render, default to 5000 locally
    app.run(host='0.0.0.0', port=port, debug=True)
