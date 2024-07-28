from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=50)
    mobile_phone = models.CharField(max_length=50)
    password = models.CharField(max_length=128) 
    balance = models.FloatField(default=0.0)
