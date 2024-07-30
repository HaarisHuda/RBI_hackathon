from django.contrib import admin
from .models import  TransactionModel, CustomerAccount, CreditCardModel, DebitCardModel , NetBankingDetailsModel, Report, VirtualCreditCardModel, VirtualDebitCardModel

# admin.site.register(LockingSystemModel)
admin.site.register(TransactionModel)
admin.site.register(CustomerAccount)
admin.site.register(CreditCardModel)
admin.site.register(DebitCardModel)
admin.site.register(NetBankingDetailsModel)
admin.site.register(Report)
admin.site.register(VirtualDebitCardModel)
admin.site.register(VirtualCreditCardModel)