from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from products.models import Products
from .BarcodeReader import barcodeScanner
from .models import Customer as cust,billsStatus
from master.models import UOM,Tax
from .models import Itemsdetails
from django.utils import timezone
from django.core.paginator import Paginator
import random,csv,io


class Customer(View):
    def get(self, request):
        object = cust.objects.all().order_by("-id")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        custobj = cust.objects.all().filter(id=1).exists()
        return render(self.request, 'bill/Customer_details.html',{'customerdetails':page_obj,'customer':custobj})

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
        object = cust.objects.all().order_by("-id")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'bill/Customer_details.html',{'customerdetails':page_obj})

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
        tax = Tax.objects.all()
        return render(self.request, 'bill/newbill.html',
                      {'items': products_added, 'billtocustomer': customer, 'product': products, 'custid': customer,'taxs':tax})

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
            obj.itm_billnum = cust_details.billnum
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
                obj.qty = obj.qty - int(dec)
                obj.total_price = float(int(obj.products.price)) * obj.qty
                obj.save()
        return redirect('/billing/newbill/' + customer_id)


def delete_childitm(request, id):
    if request.method == 'POST':
        customer_id = request.POST.get('customerid')
        billnum = request.POST.get('billnumber')
        objectprod = Itemsdetails.objects.filter(cust=customer_id).filter(products=id).filter(itm_billnum=billnum)
        objectprod.delete()
    return redirect('/billing/newbill/' + customer_id)

def importCust_template(request):
    response = HttpResponse(content_type='text/csv')
    write = csv.writer(response)
    write.writerow(['Customer Name','Adderss','Phone Number','Email','bill num'])
    response['content-Disposition'] = 'attachment,filename="customer.csv"'
    return response

def importcustomerdata(request):
    object = cust.objects.all().order_by("-id")
    paginator = Paginator(object, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        filename = request.FILES['file']
        if filename.name.endswith('.csv'):
            data_set = filename.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                cust.objects.update_or_create(
                    sellername = 'SimpleBilling',
                    billtoname = column[0],
                    adderss = column[1],
                    phonenumber = column[2],
                    email = column[3],
                    billnum = column[4],
                    billdate = timezone.now(),
                    executvie = request.user
                )
        return render(request, 'bill/Customer_details.html',{'customerdetails':page_obj})

def calculate_total(request):
    object = cust.objects.all().order_by("-id")
    paginator = Paginator(object, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sumadd = 0
    twithtax = 0
    if request.method == 'POST':
        cid = int(request.POST.get('custid'))
        bnum = str(request.POST.get('cust_billnum'))
        status_bill = request.POST.get('status')
        tax = float(request.POST.get('taxper'))
        disc = request.POST.get('disc')
        custtobill = cust.objects.get(id=cid)
        items = Itemsdetails.objects.filter(cust_id=cid).filter(itm_billnum = bnum)
        for i in items:
            sumadd = sumadd+i.total_price
        twithtax = ((sumadd*tax)/100)+sumadd
        print(twithtax)
        #if disc is not None:
            #twithtax = (twithtax*float(disc))/100
        obj = billsStatus()
        obj.customer = custtobill
        obj.billstatus_billnum = bnum
        obj.status = status_bill
        obj.tax = tax
        obj.billspayable = twithtax
        if disc is None:
            obj.discount = 0.0
        else:
            obj.discount = float(disc)
        obj.save()
    return render(request, 'bill/Customer_details.html',{'customerdetails':page_obj})