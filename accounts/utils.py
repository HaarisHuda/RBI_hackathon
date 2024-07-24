# accounts/utils.py

import random
import string
from django.db.models import F
from .models import Report, CustomerAccount

def generate_random_card_number():
    return ''.join(random.choices(string.digits, k=16))

def generate_random_cvv():
    return random.randint(100, 999)

def generate_random_pin():
    return ''.join(random.choices(string.digits, k=4))

def generate_random_account_number():
    return ''.join(random.choices(string.digits, k=12))

def handle_report(receiver_upi, transaction, description, image_1, image_2):
    report, created = Report.objects.get_or_create(receiver_upi=receiver_upi, transaction=transaction)
    report.report_count = F('report_count') + 1
    report.description = description
    if image_1:
        report.image_1 = image_1
    if image_2:
        report.image_2 = image_2
    report.save()

    # Refresh the report instance to get the updated report_count value
    report.refresh_from_db()

    if report.report_count >= 10:
        customer_account = CustomerAccount.objects.filter(user__upi_id=receiver_upi).first()
        if customer_account:
            customer_account.is_frozen = True
            customer_account.save()