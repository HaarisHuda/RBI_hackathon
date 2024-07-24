from django.db import models
import datetime
from django.utils import timezone
from users.models import User
from django.conf import settings


# Create your models here.
class CreditCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    pin = models.CharField(max_length=4, null=True, blank=True)  # Add PIN field
    expiration_date = models.DateField()
    is_locked = models.BooleanField()  # Add is_locked field

    def __str__(self):
        return f"Credit Card {self.card_number} for {self.card_holder_name}"

class DebitCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4, null=True, blank=True)  # Add PIN field
    is_locked = models.BooleanField()  # Add is_locked field

    def __str__(self):
        return f"Debit Card {self.card_number} for {self.card_holder_name}"

class NetBankingDetailsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    is_locked = models.BooleanField()  # Add is_locked field

    def __str__(self):
        return f"Net Banking Details for {self.bank_name}"
    


class VirtualCreditCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Add timestamp

    def __str__(self):
        return f"Virtual Credit Card {self.card_number} for {self.card_holder_name}"

class VirtualDebitCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Add timestamp

class CustomerAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Assuming '1' is a valid user ID
    customer_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, default="defaultemail@email.com")
    phnno = models.IntegerField(null=True)
    credit_score = models.IntegerField()
    customer_location = models.CharField(max_length=255)
    customer_gender = models.CharField(max_length=7)
    customer_age = models.IntegerField()
    customer_account_balance = models.FloatField()
    is_frozen = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer Account {self.customer_id} - {self.name}"
    def __str__(self):
        return f"Customer Account {self.customer_id} - {self.name}"
    

class TransactionModel(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    sender_phnno = models.IntegerField(default=1234)
    receiver_phno = models.IntegerField(default=1234)
    sender_upi = models.CharField(max_length=255)
    receiver_upi = models.CharField(max_length=255)
    receiver_account = models.ForeignKey(CustomerAccount, related_name='received_transactions', on_delete=models.CASCADE, null=True)
    customer_id = models.CharField(max_length=255)
    customer_dob = models.DateField(null=True)
    customer_gender = models.CharField(max_length=7, null=True)
    customer_location = models.CharField(max_length=255, null=True)
    customer_account_balance = models.FloatField()
    transaction_date = models.DateField(auto_now_add=True)
    transaction_time = models.BigIntegerField()
    transaction_amount = models.FloatField()
    device_name = models.CharField(max_length=255, default="abc")
    def __str__(self):
        return self.transaction_id

    # receiver = models.ForeignKey(User, on_delete=models.CASCADE, default="1")

   
    def get_transaction_datetime(self):
        """
        Convert Unix timestamp to datetime.
        """
        return datetime.datetime.fromtimestamp(self.transaction_time)



# accounts/models.py
class Report(models.Model):
    receiver_upi = models.CharField(max_length=255)
    report_count = models.IntegerField(default=0)
    transaction = models.ForeignKey(TransactionModel, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_1 = models.ImageField(upload_to='report_images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='report_images/', null=True, blank=True)

    def __str__(self):
        return f"Reports for UPI ID {self.receiver_upi}"
