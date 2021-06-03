from django.db import models

# Create your models here.


class Product(models.Model):
    CustomerId = models.CharField(max_length=15)
    ProductName = models.CharField(max_length=30)
    Domain = models.CharField(max_length=100)
    StartDate = models.DateField()
    Duration = models.IntegerField()