from django.urls import path
from . import views

urlpatterns = [
    path('predict_spam/', views.SMSPredictView.as_view()),
]
