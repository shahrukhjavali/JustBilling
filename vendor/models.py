from django.db import models
from accounts.models import User

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    adderss = models.CharField(max_length=250)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    code = models.CharField(max_length=6)
    email = models.EmailField()
    status = models.BooleanField()
    createdby = models.ForeignKey(User,on_delete=models.CASCADE,related_name='vcreated')
    creationdate = models.DateTimeField()
    last_updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='vupdated')
    last_update_date = models.DateTimeField()
