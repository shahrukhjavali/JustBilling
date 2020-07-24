from django.db import models
from accounts.models import User

class UOM(models.Model):
    name=models.CharField(max_length=3)
    desc=models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    createdby = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uomcreated')
    creationdate = models.DateTimeField()
    last_update_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uomupdated')
    last_update_date = models.DateTimeField()

class Tax(models.Model):
    name=models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    percentage = models.FloatField()
    status = models.BooleanField(default=True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taxcreated')
    creationdate = models.DateTimeField()
    last_update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taxupdated')
    last_update_date = models.DateTimeField()

