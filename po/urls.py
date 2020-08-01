from django.urls import path
from .views import  po,addPo,addchildItems,deletechilditm,editchildqty,donePo,sendemailToVendor,renderPolist

urlpatterns = [
    path('polist',po,name='polist'),
    path('addpoitm/<int:id>',addPo.as_view(),name='addpoitm'),
    path('addchild/<int:id>',addchildItems,name='addpochild'),
    path('delete/<int:id>',deletechilditm,name='delete'),
    path('edititems/<int:id>',editchildqty,name='edititmqty'),
    path('donepo/<int:id>',donePo,name='donepo'),
    path('send/<int:id>',sendemailToVendor,name='send'),
    path('addpo',renderPolist,name='addpo'),
]