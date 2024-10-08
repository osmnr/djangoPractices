from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class City(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name
    

class UserCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, null=True, blank=True )

    def __str__(self):
        return self.city.name