from django.db import models
import joblib

class SpamDetector:
    def __init__(self):
        self.model = joblib.load("spam_sms_detector.pkl")  # Replace with correct path
        self.vectorizer = joblib.load("tfidf_vectorizer.pkl")  # Replace with correct path

    def predict(self, sms):
        new_sms_features = self.vectorizer.transform([sms])
        prediction = self.model.predict(new_sms_features)[0]
        if prediction == 1:
            return "spam"
        else:
            return "not spam"

class SpamDetectionModel(models.Model):
    text = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    spam_not_spam = models.BooleanField()
    # risk_associated = models.FloatField()

    def __str__(self):
        return self.text
    

class TransactionPatternDetectionModel(models.Model):
    sender_location = models.CharField(max_length=255)
    sender_device_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender_upi_ac_no = models.CharField(max_length=255)
    receiver_upi_ac_no = models.CharField(max_length=255)
    sender_acc_balance = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_transaction = models.CharField(max_length=255)
    frequency_of_transaction = models.IntegerField()
    fraud_not_fraud = models.BooleanField()

    def __str__(self):
        return f"{self.sender_device_id} to {self.receiver_upi_ac_no} - {self.amount}"