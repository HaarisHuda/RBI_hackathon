from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Report, TransactionModel, VirtualDebitCardModel , VirtualCreditCardModel, CustomerAccount, CreditCardModel, DebitCardModel, NetBankingDetailsModel
from .serializers import ReportSerializer, TransactionSerializer, CreditCardSerializer, DebitCardSerializer, VirtualCreditCardSerializer, VirtualDebitCardSerializer,  LockStatusSerializer
import random
from datetime import date, time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_random_card_number,  generate_random_pin, generate_random_cvv, handle_report
from apscheduler.schedulers.background import BackgroundScheduler
from users.models import User
from django.utils import timezone
import logging
import traceback
import uuid
from django.utils import timezone
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet


class UserTransactionsView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TransactionModel.objects.filter(
            Q(sender_upi=user.upi_id) | Q(receiver_upi=user.upi_id)
        )

# Configure logging
logger = logging.getLogger(__name__)

def remove_expired_virtual_cards():
    expiry_time = timezone.now() - timezone.timedelta(minutes=5)
    VirtualCreditCardModel.objects.filter(created_at__lt=expiry_time).delete()
    VirtualDebitCardModel.objects.filter(created_at__lt=expiry_time).delete()
    # VirtualNetBankingDetailsModel.objects.filter(created_at__lt=expiry_time).delete()

scheduler = BackgroundScheduler()
scheduler.add_job(remove_expired_virtual_cards, 'interval', minutes=5)
scheduler.start()

class GenerateRandomCreditCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            credit_card = VirtualCreditCardModel.objects.create(
                user=user,
                card_number=generate_random_card_number(),
                card_holder_name=f'{user.name}',
                expiration_date=timezone.now().date() + timezone.timedelta(days=365*5),
                cvv=generate_random_cvv(),
                pin=generate_random_pin()
            )
            serializer = VirtualCreditCardSerializer(credit_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating credit card: {e}")
            logger.error(traceback.format_exc())
            return Response({'error': 'An error occurred while generating the credit card'}, status=500)

class GenerateRandomDebitCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            debit_card = VirtualDebitCardModel.objects.create(
                user=user,
                card_number=generate_random_card_number(),
                card_holder_name=f'{user.name}',
                expiration_date=timezone.now().date() + timezone.timedelta(days=365*5),
                cvv=generate_random_cvv(),
                pin=generate_random_pin()
            )
            serializer = VirtualDebitCardSerializer(debit_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating debit card: {e}")
            logger.error(traceback.format_exc())
            return Response({'error': 'An error occurred while generating the debit card'}, status=500)
        
class ReportTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        description = request.data.get('description')
        image_1 = request.FILES.get('product_image_1', None)
        image_2 = request.FILES.get('product_image_2', None)

        # Find the transaction to get the receiver
        try:
            transaction = TransactionModel.objects.get(transaction_id=transaction_id)
            receiver = transaction.receiver
        except TransactionModel.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        report_details = {
            'transaction_id': transaction_id,
            'description': description,
            'image_1': image_1,
            'image_2': image_2,
            'receiver': receiver.id,
        }

        serializer = ReportSerializer(data=report_details)
        if serializer.is_valid():
            serializer.save()

            # Count the number of reports for the receiver
            report_count = Report.objects.filter(receiver=receiver).count()
            if report_count > 10:
                # Freeze the account
                customer_account = CustomerAccount.objects.get(CustomerId=receiver.id)
                customer_account.is_frozen = True  # Assuming you have a field 'is_frozen' to mark the account as frozen
                customer_account.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# In accounts/views.py (update the PerformTransactionView)

class PerformTransactionView(APIView):
    def post(self, request):
        data = request.data
        sender_upi = data.get('sender_upi')
        receiver_upi = data.get('receiver_upi_id')
        transaction_amount = data.get('amount')
        device_name = data.get('device_name')
        location = data.get('location')

        # Retrieve sender and receiver accounts
        try:
            sender = User.objects.get(upi_id=sender_upi)
            receiver = User.objects.get(upi_id=receiver_upi)
        except User.DoesNotExist:
            return Response({'error': 'Invalid UPI ID(s)'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve sender and receiver customer accounts
        try:
            sender_account = CustomerAccount.objects.get(user=sender)
            receiver_account = CustomerAccount.objects.get(user=receiver)
        except CustomerAccount.DoesNotExist:
            return Response({'error': 'Customer account not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the sender's or receiver's account is frozen
        if sender_account.is_frozen or receiver_account.is_frozen or sender.is_upi_locked:
            return Response({'error': 'Transaction cannot be performed. One of the accounts is frozen.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if sender has sufficient balance
        if sender_account.customer_account_balance < transaction_amount:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform transaction
        sender_account.customer_account_balance -= transaction_amount
        receiver_account.customer_account_balance += transaction_amount

        sender_account.save()
        receiver_account.save()

        # Save transaction details
        transaction = TransactionModel.objects.create(
            transaction_id=str(uuid.uuid4()),
            sender_phnno=sender.phn,
            receiver_phno=receiver.phn,
            sender_upi=sender_upi,
            receiver_upi=receiver_upi,
            customer_id=sender_account.customer_id,
            customer_location=location,
            customer_account_balance=sender_account.customer_account_balance,
            transaction_date=timezone.now().date(),
            transaction_time=int(timezone.now().timestamp()),
            transaction_amount=transaction_amount,
            device_name=device_name
        )

        return Response({'message': 'Transaction successful'}, status=status.HTTP_200_OK)

class LockStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        serializer = LockStatusSerializer(data=data)
        
        if serializer.is_valid():
            # Update credit card lock status
            CreditCardModel.objects.filter(user=user).update(is_locked=serializer.validated_data['credit'])
            
            # Update debit card lock status
            DebitCardModel.objects.filter(user=user).update(is_locked=serializer.validated_data['debit'])
            
            # Update net banking lock status
            NetBankingDetailsModel.objects.filter(user=user).update(is_locked=serializer.validated_data['net_banking'])
            
            # Update UPI lock status
            user.is_upi_locked = serializer.validated_data['upi']
            user.save()

            # Get the updated lock status for each account type
            credit_locked = CreditCardModel.objects.filter(user=user, is_locked=True).exists()
            debit_locked = DebitCardModel.objects.filter(user=user, is_locked=True).exists()
            net_banking_locked = NetBankingDetailsModel.objects.filter(user=user, is_locked=True).exists()
            upi_locked = user.is_upi_locked

            response_data = {
                "credit": credit_locked,
                "debit": debit_locked,
                "net_banking": net_banking_locked,
                "upi": upi_locked
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ReportTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        transaction_id = request.data.get('transaction_id')
        description = request.data.get('description')
        image_1 = request.FILES.get('product_image_1', None)
        image_2 = request.FILES.get('product_image_2', None)

        try:
            transaction = TransactionModel.objects.get(transaction_id=transaction_id)
            receiver_upi = transaction.receiver_upi
            handle_report(receiver_upi, transaction, description, image_1, image_2)
            return Response({'message': 'Report submitted successfully.'}, status=status.HTTP_200_OK)
        except TransactionModel.DoesNotExist:
            return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)
