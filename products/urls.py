from django.urls import path
from .views import Product,importCsv,importCsvdata

urlpatterns = [
    path('newproduct',Product.as_view(),name='newproduct'),
    path('importcsvtemp',importCsv,name='importtemplate'),
    path('importcsvdata',importCsvdata,name='importcsvdata'),
]