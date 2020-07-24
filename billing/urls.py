from django.urls import path
from .views import newBill,Customer,editItemqty,delete_childitm

urlpatterns = [
    path('newbill/<int:id>',newBill.as_view(),name='newbill'),
    path('cust',Customer.as_view(),name='cust'),
    path('editqty/<int:id>',editItemqty,name='editqty'),
    path('child_del/<int:id>',delete_childitm,name='child_del'),
]