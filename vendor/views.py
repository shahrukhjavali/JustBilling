from django.shortcuts import render,HttpResponse
from django.views.generic import View
from .models import Vendor
from django.core.paginator import Paginator
from django.utils import timezone
import random,csv,io

class createVendor(View):
    def get(self,request):
        allvendors = Vendor.objects.all()
        paginator = Paginator(allvendors, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request,'vendor/vendor.html',{'vendorlist':page_obj})

    def post(self,request):
        allvendors = Vendor.objects.all()
        paginator = Paginator(allvendors, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        vendorname = request.POST.get('vname')
        adderss = request.POST.get('adderss1')+request.POST.get('adderss2')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        obj = Vendor()
        obj.name = vendorname
        obj.adderss = adderss
        obj.phone = phone
        obj.city = city
        obj.state = state
        obj.pincode = pincode
        obj.email = email
        obj.status = True
        obj.code = str(genCode())
        obj.createdby = request.user
        obj.creationdate = timezone.now()
        obj.last_updated_by = request.user
        obj.last_update_date = timezone.now()
        obj.save()
        return render(self.request, 'vendor/vendor.html', {'vendorlist': page_obj})

def genCode():
    number = random.randint(1,1000)
    return number

def importCsvvendor(request):
    response = HttpResponse(content_type='text/csv')
    write = csv.writer(response)
    write.writerow(['vendor Name','Adderss','Phone','City','State','Pincode'])
    response['content-Disposition'] = 'attachment,filename="vendor.csv"'
    return response

def importCsvdata(request):
    object = Vendor.objects.all().order_by("-last_update_date")
    paginator = Paginator(object, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET':
        request, 'vendor/vendor.html', {'vendorlist': page_obj}
    if request.method == 'POST':
        filename = request.FILES['file']
        if filename.name.endswith('.csv'):
            data_set = filename.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                created = Vendor.objects.update_or_create(
                    name=column[0],
                    adderss=column[1],
                    phone=column[2],
                    city=column[3],
                    state=column[4],
                    pincode=column[5],
                    code=str(genCode()),
                    status=True,
                    createdby=request.user,
                    creationdate=timezone.now(),
                    last_updated_by=request.user,
                    last_update_date=timezone.now()
                )
            return render(request, 'vendor/vendor.html', {'vendorlist': page_obj})