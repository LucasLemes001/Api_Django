from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from passlib.hash import pbkdf2_sha256
from .models import UserModel

class UserRegisteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","username","email"] # Not include password in the response Beacause NEVER RETURN PASSWORDS


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = UserModel.objects.get(username=username)

            if pbkdf2_sha256.verify(password, user.password):
                
                refresh = RefreshToken.for_user(user)

                return {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }
            else:
                raise serializers.ValidationError("Invalid username or password")
        
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")