from .permissions import PostOnlyPermission
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import User
from .renderers import UserRenderer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status


# manually generate token 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    # renderer_classes= [UserRenderer]
    def post(self, request, format =None):
        serializer = UserRegistrationSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token= get_tokens_for_user(user)
            return Response({'token': token},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    # renderer_classes= [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                response_data = {
                    'refresh': tokens['refresh'],
                    'access': tokens['access'],
                    'msg': 'login success'
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AllUserDetail(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    

class UserProfileDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    # For fetching details of the logged in user
    def get(self, request):
        user = request.user
        serializer_data = UserDetailSerializer(user).data
        return Response(serializer_data, status=status.HTTP_200_OK)