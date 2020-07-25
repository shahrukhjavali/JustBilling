from django.urls import path
from .views import createUomview,importUomtemplate,importUomdata

urlpatterns = [
    path('createuom',createUomview.as_view(),name='createuom'),
    path('importuomtemplate',importUomtemplate,name='importuomtemplate'),
    path('importuomdata',importUomdata,name='importuomdata'),
]