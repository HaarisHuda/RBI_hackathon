# mlmodel/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SMSSerializer
from .predict import predict_sms

class SMSPredictView(APIView):
    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            sms_text = serializer.validated_data['text']
            prediction = predict_sms(sms_text)
            if prediction == 1 or prediction == "1":
                result = "This SMS is likely spam." 
            else:
                result="This SMS is likely not spam."
            return Response({"prediction": prediction, "result": result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
