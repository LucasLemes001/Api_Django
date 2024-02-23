from rest_framework import serializers
from .models import UserModel

class UserRegisteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","username","email"] # Not include password in the response Beacause NEVER RETURN PASSWORDS