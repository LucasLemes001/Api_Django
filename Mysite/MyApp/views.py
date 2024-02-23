from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserRegisteredSerializer
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
            
            username = request.data['username'],
            email = request.data['email'],
            password = pbkdf2_sha256.hash(request.data['password']),
        )

        return Response({"message": "User created successfully", "User": new_user.username})
    

class UserListView(APIView):

    def get(self, request):

        users = UserModel.objects.all()

        serializer = UserRegisteredSerializer(users,many=True)
        return Response(serializer.data)
    


class UnregisterView(APIView):

    def delete(self, request, user_id):
        try:
            user = UserModel.objects.get(id=user_id)

            user.delete()
            return Response({"message": "User deleted successfully"})
        except UserModel.DoesNotExist:
            return Response({"message": "User not found! Verify the id"})
