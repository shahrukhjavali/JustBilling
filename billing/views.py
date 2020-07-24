from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from products.models import Products
from .BarcodeReader import barcodeScanner
from .models import Customer as cust
from master.models import UOM
from .models import Itemsdetails
from django.utils import timezone
import random


class Customer(View):
    def get(self, request):
        return render(self.request, 'bill/Customer_details.html')

    def post(self, request):
        name = request.POST.get('cust_name')
        adderss1 = request.POST.get('adderss1')
        adderss2 = request.POST.get('adderss2')
        phone = request.POST.get('phone')
        email = request.POST.get('Email')
        obj = cust()
        obj.sellername = 'SimpleBilling'
        obj.billtoname = name
        obj.adderss = adderss1 + adderss2
        obj.phonenumber = phone
        obj.email = email
        obj.billnum = self.genarateBillnum()
        obj.billdate = timezone.now()
        obj.executvie = request.user
        obj.save()
        return render(self.request, 'bill/Customer_details.html')

    def genarateBillnum(self):
        billnum = random.randrange(1, 9000)
        day = str(timezone.now().date())
        return day + str(billnum)


class newBill(View):

    def get(self, request, **kwargs):
        customer = cust.objects.get(id=kwargs['id'])
        bar_code = barcodeScanner()
        products = Products.objects.filter(Barcode=bar_code)
        products_added = Itemsdetails.objects.filter(cust=kwargs['id'])
        return render(self.request, 'bill/newbill.html',
                      {'items': products_added, 'billtocustomer': customer, 'product': products, 'custid': customer})

    def post(self, request, **kwargs):
        id = request.POST.get('pid')
        qty = request.POST.get('pqty')
        uom = request.POST.get('uom')
        cust_details = cust.objects.get(id=kwargs['id'])
        prod = Products.objects.get(id=id)
        uomprod = UOM.objects.get(name=uom)
        availble_prod = Itemsdetails.objects.filter(cust=kwargs['id']).filter(products=prod)
        if availble_prod.exists():
            oldobj = availble_prod[0]
            oldobj.qty = float(int(qty)) + oldobj.qty
            oldobj.total_price = ((float(int(prod.price)) * float(int(oldobj.qty))))
            oldobj.save()
        else:
            obj = Itemsdetails()
            obj.cust = cust_details
            obj.products = prod
            obj.qty = float(int(qty))
            obj.uom = uomprod
            obj.total_price = ((float(int(prod.price)) * float(int(qty))))
            obj.save()
        products_added = Itemsdetails.objects.filter(cust=kwargs['id'])
        return redirect('/billing/newbill/' + str(kwargs['id']), {'items': products_added, 'custid': int(kwargs['id'])})


def editItemqty(request, id):
    if request.method == 'POST':
        customer_id = request.POST.get('customerid')
        dec = int(request.POST.get('decqty'))
        objectprod = Itemsdetails.objects.filter(cust=customer_id).filter(products=id)
        if objectprod.exists():
            obj = objectprod[0]
            if obj.qty >= dec:
                obj.qty = obj.qty + int(dec)
                obj.total_price = float(int(obj.products.price)) * obj.qty
                obj.save()
        return redirect('/billing/newbill/' + customer_id)


def delete_childitm(request, id):
    if request.method == 'POST':
        customer_id = request.POST.get('customerid')
        objectprod = Itemsdetails.objects.filter(cust=customer_id).filter(products=id)
        objectprod.delete()
    return redirect('/billing/newbill/' + customer_id)
