from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserModel
from passlib.hash import pbkdf2_sha256
# Create your views here.
class RegisterView(APIView):

    def post(self, request):

        if UserModel.objects.filter(username=request.data['username']).exists():
            return Response({"message": "Username already exists"})
        
        if UserModel.objects.filter(email=request.data['email']).exists():
            return Response({"message": "Email already exists"})

        new_user = UserModel.objects.create(
            id = request.data['id'],
            username = request.data['username'],
            email = request.data['email'],
            password = pbkdf2_sha256.hash(request.data['password']),
        )

        return Response({"message": "User created successfully", "User": new_user.username})
    