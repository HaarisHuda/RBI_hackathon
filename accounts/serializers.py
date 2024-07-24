from rest_framework import serializers
from .models import Report, TransactionModel, CreditCardModel , DebitCardModel, VirtualCreditCardModel , VirtualDebitCardModel 

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'

class LockStatusSerializer(serializers.Serializer):
    credit = serializers.BooleanField()
    debit = serializers.BooleanField()
    net_banking = serializers.BooleanField()
    upi = serializers.BooleanField()

    
class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardModel
        fields = '__all__'

class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCardModel
        fields = '__all__'

class VirtualCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualCreditCardModel
        fields = '__all__'

class VirtualDebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualDebitCardModel
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


