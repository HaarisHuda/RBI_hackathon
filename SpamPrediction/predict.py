# myapp/predict.py
import joblib
import os

# Get the absolute path of the directory where the current script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths to the model and vectorizer files
model_path = os.path.join(base_dir, 'spam_sms_detector.pkl')
vectorizer_path = os.path.join(base_dir, 'tfidf_vectorizer.pkl')  # Note the space before .pkl

# Load the model and vectorizer
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def predict_sms(sms_text):
    new_sms_features = vectorizer.transform([sms_text])
    prediction = model.predict(new_sms_features)[0]
    # print(prediction)
    return prediction
# print(predict_sms("Congratulations! Your credit score entitles you to a no-interest Visa credit card. Click here to claim: [Link]"))