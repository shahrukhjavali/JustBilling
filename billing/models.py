from django.db import models
from accounts.models import User
from products.models import Products
from master.models import UOM

class Customer(models.Model):
    sellername = models.CharField(max_length=30)
    billtoname = models.CharField(max_length=30)
    adderss = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=10)
    email = models.EmailField()
    billnum = models.CharField(max_length=30)
    billdate = models.DateTimeField()
    executvie = models.ForeignKey(User,on_delete=models.CASCADE)

class Itemsdetails(models.Model):
    cust = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='cust')
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    qty = models.FloatField()
    uom = models.ForeignKey(UOM,on_delete=models.CASCADE)
    total_price = models.FloatField()

class billsStatus(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    paymentType = models.CharField(max_length=30)
    tax = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    billspayable = models.FloatField()

