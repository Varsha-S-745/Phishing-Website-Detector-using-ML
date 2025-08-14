import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from feature_extraction import extract_features

data = [
    ["https://www.google.com", 0],
    ["http://malicious-site.com/steal-password", 1],
    ["https://secure-login.bank.com", 0],
    ["http://phishing-login.com@evil.com", 1],
    ["https://update-paypal.com.fake-domain.ru", 1]
]

df = pd.DataFrame(data, columns=["url", "label"])

X = [extract_features(url) for url in df['url']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "phishing_model.pkl")
print("Model trained and saved!")
