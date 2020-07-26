from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .models import UOM,Tax
from django.core.paginator import Paginator
from django.utils import timezone
import csv, io


# from django.contrib.auth.decorators import login_required
class createTaxview(View):
    def get(self,request):
        object = Tax.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request,'tax/tax.html', {'taxlist': page_obj})

    def post(self,request):
        object = Tax.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        name = request.POST.get('tname')
        desc = request.POST.get('desc')
        percentage = float(request.POST.get('per'))
        obj = Tax()
        obj.name = name
        obj.description = desc
        obj.percentage = percentage
        obj.status = True
        obj.createdby = request.user
        obj.creationdate = timezone.now()
        obj.last_update_by = request.user
        obj.last_update_date = timezone.now()
        obj.save()
        return render(self.request, 'tax/tax.html', {'taxlist': page_obj})

class createUomview(View):
    def get(self, request):
        object = UOM.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'master/master.html', {'uomlist': page_obj})

    def post(self, request):
        uomname = request.POST.get('uom_name')
        description = request.POST.get('desc')
        obj = UOM()
        obj.name = uomname
        obj.desc = description
        obj.createdby = request.user
        obj.creationdate = timezone.now()
        obj.last_update_by = request.user
        obj.last_update_date = timezone.now()
        obj.save()
        object = UOM.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'master/master.html', {'uomlist': page_obj})


def importUomtemplate(request):
    response = HttpResponse(content_type='text/csv')
    write = csv.writer(response)
    write.writerow(['name', 'description'])
    response['content-Disposition'] = 'attachment,filename="uom.csv"'
    return response


def importUomdata(request):
    object = UOM.objects.all().order_by("-last_update_date")
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
                UOM.objects.update_or_create(
                    name=column[0],
                    desc=column[1],
                    status=True,
                    createdby = request.user,
                    creationdate = timezone.now(),
                    last_update_by = request.user,
                    last_update_date = timezone.now()
                )
        return render(request, 'master/master.html', {'uomlist': page_obj})

