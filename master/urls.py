from django.urls import path
from .views import createUomview

urlpatterns = [
    path('createuom',createUomview.as_view(),name='createuom'),

]