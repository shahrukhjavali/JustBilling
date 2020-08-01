from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Inventory,DamgedStock
from po.models import Po,poItems,potracker
from products.models import Products
from master.models import UOM
from django.utils import timezone

class createInv(View):
    def get(self,request):
        object = Inventory.objects.all().order_by("-last_update_date")
        paginator = Paginator(object, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cnt = Po.objects.count()
        return render(self.request,'inventory/inventory_list.html',{'liststock':page_obj,'count':cnt})


def addpoitminv(request,ponum):
    po = Po.objects.get(ponum=ponum)
    poitms = poItems.objects.filter(ponum=ponum).filter(podetails=po)
    uomlist = UOM.objects.all()
    if request.method == 'POST':
        prodid = request.POST.get('prod')
        uom = request.POST.get('uom')
        print(uom)
        print(prodid)
        inventoryitm = Inventory.objects.filter(invproducts=Products.objects.get(id=int(prodid)))
        #dmginvitem = DamgedStock.objects.filter(dmgproducts=prodid)
        stock = float(request.POST.get('stock'))
        if inventoryitm.exists():
            inventoryitm[0].stock = inventoryitm.stock+stock
            inventoryitm[0].last_update_date = timezone.now()
            inventoryitm[0].save()
        else:
            Invitmadd = Inventory()
            Invitmadd.invproducts = Products.objects.get(id=int(prodid))
            Invitmadd.invuom = UOM.objects.get(id=int(uom))
            Invitmadd.stock = stock
            Invitmadd.invponum = ponum
            Invitmadd.created_by = request.user
            Invitmadd.last_update_date = timezone.now()
            Invitmadd.save()
            obj = potracker.objects.get(po_num=ponum)
            obj.status = 'Completed'
            obj.save()
    return render( request,'inventory/inventory_list.html',{'poitms':poitms,'pod':po,'uomlist':uomlist})