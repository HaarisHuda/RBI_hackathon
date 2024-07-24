from django.contrib import admin
from .models import SpamDetectionModel, TransactionPatternDetectionModel
# Register your models here.
admin.site.register(SpamDetectionModel)
admin.site.register(TransactionPatternDetectionModel)