from django.db import models
from vendor.models import Vendor
from accounts.models import User
from products.models import Products
from master.models import UOM

class Po(models.Model):
    ponum = models.CharField(max_length=30)
    date = models.DateTimeField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendordetails')
    shipto = models.CharField(max_length=200)
    shipcity = models.CharField(max_length=50)
    shipstate = models.CharField(max_length=50)
    shippincode = models.CharField(max_length=10)
    poreqbydate = models.DateTimeField()
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pocreated')
    creation_date = models.DateTimeField()

class poItems(models.Model):
    podetails = models.ForeignKey(Po, on_delete=models.CASCADE,related_name='po')
    ponum = models.CharField(max_length=30)
    po_items = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='items')
    qty = models.FloatField()
    uom = models.ForeignKey(UOM,on_delete=models.CASCADE,related_name='pouom')
    subtotal = models.FloatField()

class potracker(models.Model):
    po_num = models.CharField(max_length=30)
    podetail = models.ForeignKey(Po,on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    tax = models.FloatField()
    disc = models.FloatField()
    pototal = models.FloatField()
