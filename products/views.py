from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Products
import random, os, csv, io
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from django.utils import timezone


class Product(View):
    def get(self, request):
        object = Products.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product/products.html', {'addproducts': page_obj})

    def post(self, request):
        object = Products.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        name = request.POST.get('prodname')
        description = request.POST.get('desc')
        catagory = request.POST.get('catagory')
        mfg_date = request.POST.get('mfg_date')
        exp_date = request.POST.get('Exp_date')
        price = request.POST.get('price')
        obj = Products()
        obj.Name = name
        obj.description = description
        obj.catagory = catagory
        count = Products.objects.count() + 1
        obj.Barcode = genBarcode(count)
        obj.mfgdate = mfg_date
        obj.expdate = exp_date
        obj.price = float(price)
        obj.status = True
        obj.createdby = request.user
        obj.creationdate = timezone.now()
        obj.last_update_by = request.user
        obj.last_update_date = timezone.now()
        obj.save()
        return render(request, 'product/products.html', {'addproducts': page_obj})


def genBarcode(count):
    num = random.randrange(1, 9000000000000)
    print(num)
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bar_code = barcode.EAN13(str(num), writer=ImageWriter())
    file = open('./static/images/product/' + str(count) + '.svg', "wb")
    bar_code.write(file, BytesIO())
    return num


def importCsv(request):
    response = HttpResponse(content_type='text/csv')
    write = csv.writer(response)
    write.writerow(['Name', 'description', 'catagory', 'mfgdate', 'expdate', 'price'])
    response['content-Disposition'] = 'attachment,filename="products.csv"'
    return response


def importCsvdata(request):
    object = Products.objects.all().order_by("-last_update_date")
    paginator = Paginator(object, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET':
        request, 'product/products.html', {'addproducts': page_obj}
    if request.method == 'POST':
        filename = request.FILES['file']
        if filename.name.endswith('.csv'):
            data_set = filename.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                if column[3] is "" or column[4]:
                    val1 = None
                    val2 = None
                else:
                    val1 = column[3]
                    val2 = column[4]
                created = Products.objects.update_or_create(
                    Name=column[0],
                    description=column[1],
                    catagory=column[2],
                    Barcode=genBarcode(object.count() + 1),
                    mfgdate=val1,
                    expdate=val2,
                    price=float(column[5]),
                    status=True,
                    createdby=request.user,
                    creationdate=timezone.now(),
                    last_update_by=request.user,
                    last_update_date=timezone.now()
                )
            return render(request, 'product/products.html', {'addproducts': page_obj})
