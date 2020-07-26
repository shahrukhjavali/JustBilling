from django.urls import path
from .views import createVendor,importCsvvendor,importCsvdata

urlpatterns = [
    path('createnew',createVendor.as_view(),name='createnew'),
    path('importcsv_vendor',importCsvvendor,name='importcsv_vendor'),
    path('importvendordata',importCsvdata,name='importvendordata'),
]