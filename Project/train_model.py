from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import joblib
import logging

from feature_extraction import extract_features

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    model = joblib.load("phishing_model.pkl")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    raise

def is_valid_url(url):
    try:
        result = urlparse(url)
        return bool(result.scheme and result.netloc)
    except Exception:
        return False

@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None
    confidence = None
    error = None

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if not url:
            error = "Please enter a URL."
            return render_template(
                "index.html",
                error=error
            )

        if not is_valid_url(url):
            error = "Invalid URL format."
            return render_template(
                "index.html",
                error=error
            )

        try:
            features = [extract_features(url)]

            pred = model.predict(features)[0]

            if hasattr(model, "predict_proba"):
                confidence = round(
                    max(model.predict_proba(features)[0]) * 100,
                    2
                )

            prediction = (
                "Phishing Website 🚨"
                if pred == 1
                else "Legitimate ✅"
            )

            logging.info(
                f"WEB | URL: {url} | Prediction: {prediction}"
            )

        except Exception as e:
            logging.error(f"Prediction Error: {e}")
            error = "An error occurred while analyzing the URL."

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        error=error
    )
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400

        url = data.get("url", "").strip()

        if not url:
            return jsonify({
                "status": "error",
                "message": "URL is required"
            }), 400

        if not is_valid_url(url):
            return jsonify({
                "status": "error",
                "message": "Invalid URL format"
            }), 400

        features = [extract_features(url)]

        pred = model.predict(features)[0]

        confidence = None

        if hasattr(model, "predict_proba"):
            confidence = round(
                max(model.predict_proba(features)[0]) * 100,
                2
            )

        prediction = (
            "Phishing"
            if pred == 1
            else "Legitimate"
        )

        logging.info(
            f"API | URL: {url} | Prediction: {prediction}"
        )

        return jsonify({
            "status": "success",
            "url": url,
            "prediction": prediction,
            "confidence": confidence
        })

    except Exception as e:

        logging.error(f"API Error: {e}")

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
