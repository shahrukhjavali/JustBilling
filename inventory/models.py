from django.db import models
from products.models import Products
from master.models import UOM
from accounts.models import User

class Inventory(models.Model):
    invproducts = models.ForeignKey(Products,on_delete=models.CASCADE)
    invuom = models.ForeignKey(UOM,on_delete=models.CASCADE)
    stock = models.FloatField()
    invponum = models.CharField(max_length=30)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    last_update_date = models.DateTimeField()

class DamgedStock(models.Model):
    dmgproducts = models.ForeignKey(Products, on_delete=models.CASCADE)
    dmguom = models.ForeignKey(UOM, on_delete=models.CASCADE)
    dmgstock = models.FloatField()
    dmgponum = models.CharField(max_length=30)
    dmgcreated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    dmg_last_update_date = models.DateTimeField()

