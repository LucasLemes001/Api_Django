from django.db import models

# Create your models here.
class UserModel(models.Model):
    id =models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)