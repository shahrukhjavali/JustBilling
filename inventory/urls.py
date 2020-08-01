from django.urls import path
from .views import createInv,addpoitminv

urlpatterns = [
    path('invlist',createInv.as_view(),name='invlist'),
    path('addinvpo/<str:ponum>',addpoitminv,name='addinvpo'),
]