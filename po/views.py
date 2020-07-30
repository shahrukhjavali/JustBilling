from django.shortcuts import render, redirect
from .models import Po, poItems, potracker
from products.models import Products
from vendor.models import Vendor
from master.models import UOM, Tax
from django.core.paginator import Paginator
from django.views.generic import View
from django.utils import timezone
import random


class addPo(View):
    def get(self, request):
        venlist = Vendor.objects.all()
        podetails = Po.objects.filter(id=1)
        products = Products.objects.all()
        objs = UOM.objects.all()
        taxs = Tax.objects.all()
        poitms = poItems.objects.filter(podetails=podetails[0]).filter(ponum=podetails[0].ponum)
        return render(self.request, 'po/addpo.html', {'venlist': venlist,
                                                      'podetails': podetails, 'products': products, 'uomobjs': objs,
                                                      'poitms': poitms, 'taxobjs': taxs})

    def post(self, request):
        obj = Po()
        obj.ponum = str(getponum())
        obj.date = timezone.now()
        obj.vendor = Vendor.objects.get(id=1)
        obj.shipto = request.POST.get('adderss1') + request.POST.get('adderss2')
        obj.shipcity = request.POST.get('city')
        obj.shipstate = request.POST.get('state')
        obj.shippincode = request.POST.get('pincode')
        obj.poreqbydate = request.POST.get('poreq_date')
        obj.createdby = request.user
        obj.creation_date = timezone.now()
        obj.save()
        return render(self.request, 'po/addpo.html', {'podetails': obj})


def po(request):
    object = Po.objects.all().order_by("-id")
    paginator = Paginator(object, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'po/polist.html', {'po': page_obj})


def addchildItems(request, id):
    if request.method == 'POST':
        po = Po.objects.get(id=id)
        ponum = po.ponum
        product = Products.objects.get(id=int(request.POST.get('product')))
        qty = float(request.POST.get('qty'))
        uom = UOM.objects.get(name=request.POST.get('uom'))
        subtotal = qty * product.price
        obj = poItems()
        obj.podetails = po
        obj.ponum = ponum
        obj.po_items = product
        obj.qty = qty
        obj.uom = uom
        obj.subtotal = subtotal
        obj.save()
    return redirect('/po/addpo')


def getponum():
    num = random.randint(1, 100000000)
    return num


def deletechilditm(request, id):
    obj = poItems.objects.get(id=id)
    obj.delete()
    return redirect('/po/addpo')


def editchildqty(request, id):
    if request.method == 'POST':
        obj = poItems.objects.get(id=id)
        obj.qty = float(request.POST.get('eqty'))
        obj.subtotal = obj.qty * obj.po_items.price
        obj.save()
    return redirect('/po/addpo')


def donePo(request,id):
    if request.method == 'POST':
        PO = Po.objects.get(id=id)
        obj = potracker()
        obj.ponum = PO.ponum
        obj.podetail = PO
        obj.status = request.POST.get('status')
        obj.tax = float(request.POST.get('tax'))
        obj.disc = float(request.POST.get('disc'))
        items = poItems.objects.filter(podetails=PO).filter(ponum=PO.ponum)
        total = 0
        for i in items:
            total = ((i.subtotal*obj.tax)/100)+i.subtotal
        obj.pototal = total
        obj.save()
    return redirect('/po/addpo')