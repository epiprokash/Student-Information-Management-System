from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from . import serializers


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class UserAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        data = serializers.UserSerializer(user).data
        return Response(
            status=status.OK,
            data=data
        )
    


class RegisterView(APIView):
    def post(self, request, pk):
        serializer = serializers.RegisterSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_201_CREATED, serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST, serializer.errors)


class LoginView(APIView):
    def post(self, request, pk):
        serializer = serializers.LoginSerializer(request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    def post(self, request):
        serializer = serializers.LogoutSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
