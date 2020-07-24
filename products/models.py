from django.db import models
from accounts.models import User

class Products(models.Model):
    Name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    catagory = models.CharField(max_length=20)
    Barcode = models.CharField(max_length=25)
    mfgdate = models.DateField(blank=True,null=True)
    expdate = models.DateField(blank=True,null=True)
    price = models.FloatField()
    status = models.BooleanField()
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='porductcreated')
    creationdate = models.DateTimeField()
    last_update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productupdated')
    last_update_date = models.DateTimeField()

