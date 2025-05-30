from django.db import models

# Create your models here
from django.contrib.auth.models import User

class Transactions(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    type          = models.CharField(max_length=10)
    amount        = models.DecimalField(max_digits=10, decimal_places=2)
    datetime      = models.DateTimeField(auto_now=True)

class Budget(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE)
    month            = models.IntegerField()
    year             = models.IntegerField()
    income           = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    expense          = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)