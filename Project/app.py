from flask import Flask, render_template, request
import joblib
from feature_extraction import extract_features

app = Flask(__name__)
model = joblib.load("phishing_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        url = request.form["url"]
        features = [extract_features(url)]
        pred = model.predict(features)[0]
        prediction = "Phishing Website 🚨" if pred == 1 else "Legitimate ✅"
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
