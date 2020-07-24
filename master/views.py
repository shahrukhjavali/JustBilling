from django.shortcuts import render
from django.views.generic import View
from .models import UOM
from django.utils import timezone
from django.contrib.auth.decorators import login_required

class createUomview(View):
    def get(self,request):
        return render(self.request,'master/master.html')

    @login_required
    def post(self,request):
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
        return render(self.request, 'master/master.html')

