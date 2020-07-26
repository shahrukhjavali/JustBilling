from django.urls import path
from .views import createUomview,importUomtemplate,importUomdata,createTaxview

urlpatterns = [
    path('createuom',createUomview.as_view(),name='createuom'),
    path('importuomtemplate',importUomtemplate,name='importuomtemplate'),
    path('importuomdata',importUomdata,name='importuomdata'),
    path('createtax',createTaxview.as_view(),name='createtax'),
]