from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class People(models.Model):
    image = models.ImageField(upload_to ='uploads/')
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    caption = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
