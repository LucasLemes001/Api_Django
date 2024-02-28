from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserRegisteredSerializer, LoginSerializer
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




class LoginView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        
        return Response(serializer.errors, status=400)
    

            

class LogoutView(APIView):

    def post(self, request):
        if "access_token" in request.data and "refresh_token" in request.data:
            access_token = request.data["access_token"]
            refresh_token = request.data["refresh_token"]

        try: 
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "User logged out successfully"})
        except:
            return Response({"message":" Invalid refresh token"}), 400
        
        else:
            return Response ({"message":"Access token and refresh token are required"}), 400
        

class RefreshView(APIView):

    def post(self, request):
        if "refresh_token" in request.data:
            refresh_token = request.data["refresh_token"]
        else:
            return Response({"message": "Refresh token is required"}), 400

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({"access_token": access_token})
        except:
            return Response({"message": "Invalid refresh token"}), 400