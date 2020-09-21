from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SignUp(models.Model):
    name = models.CharField(max_length=264,unique=True)
    email = models.EmailField(max_length=264,unique=True)
    text = models.CharField(max_length=264,unique=True)

class Registration(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)
    paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    