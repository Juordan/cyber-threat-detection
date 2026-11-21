import joblib
import pandas as pd
import json

from preprocessors.email_text_preprocessor import clean_email_text
from preprocessors.url_feature_extractor import extract_url_features

# =====================================================
# LOAD MODELS
# =====================================================

sms_model = joblib.load("models/best_sms_phishing_model.pkl")
email_model = joblib.load("models/email_model.pkl")
url_model = joblib.load("models/url_model.pkl")

print("=" * 60)
print("TEST PREDIKSI CYBER THREAT DETECTION")
print("=" * 60)

# =====================================================
# 1. SMS DETECTION
# =====================================================

sms_text = "Congratulations! You have won a free prize. Click this link now!"

sms_input = pd.DataFrame([{
    "TEXT": sms_text,
    "URL": 1,
    "EMAIL": 0,
    "PHONE": 0,
    "TEXT_LENGTH": len(sms_text)
}])

sms_prediction = sms_model.predict(sms_input)[0]

sms_labels = {
    0: "Ham (Safe SMS)",
    1: "Smishing"
}

print("\n[SMS DETECTION]")
print("Input:", sms_text)
print("Prediction:", sms_labels[int(sms_prediction)])

# =====================================================
# 2. EMAIL DETECTION
# =====================================================

email_text = """
Dear Customer,

Your account has been suspended.
Please verify your account immediately.

Click here to restore your access.
"""

cleaned_email = clean_email_text(email_text)

email_prediction = email_model.predict([cleaned_email])[0]

email_labels = {
    0: "Safe Email",
    1: "Phishing Email"
}

print("\n[EMAIL DETECTION]")
print("Prediction:", email_labels[int(email_prediction)])

# =====================================================
# 3. URL DETECTION
# =====================================================

url_text = "https://example.com/login"

url_features = extract_url_features(url_text)

with open("preprocessors/url_feature_names.json", "r") as file:
    feature_names = json.load(file)

url_input = pd.DataFrame(
    [[url_features[name] for name in feature_names]],
    columns=feature_names
)

url_prediction = url_model.predict(url_input)[0]

url_labels = {
    0: "Legitimate",
    1: "Phishing"
}

print("\n[URL DETECTION]")
print("Input:", url_text)
print("Prediction:", url_labels[int(url_prediction)])

print("\n" + "=" * 60)
print("SELESAI TEST PREDIKSI")
print("=" * 60)
