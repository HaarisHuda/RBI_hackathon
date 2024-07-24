from django.urls import path
from .views import UserTransactionsView,GenerateRandomCreditCardView, GenerateRandomDebitCardView, ReportTransaction, PerformTransactionView, LockStatusUpdateView, ReportTransactionView



urlpatterns = [
    path('user-transactions/', UserTransactionsView.as_view(), name='user-transactions'),
    path('generate-random-credit-card/', GenerateRandomCreditCardView.as_view(), name='generate-random-credit-card'),
    path('generate-random-debit-card/', GenerateRandomDebitCardView.as_view(), name='generate-random-debit-card'),
    path('report/', ReportTransaction.as_view(), name='report-transaction'),
    path('perform-transaction/', PerformTransactionView.as_view(), name='perform-transaction'),
    path('update-lock-status/', LockStatusUpdateView.as_view(), name='update-lock-status'),
    path('report-transaction/', ReportTransactionView.as_view(), name='report-transaction'),
]
