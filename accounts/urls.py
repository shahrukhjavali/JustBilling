from django.urls import path
from .views import loginView

urlpatterns = [
    path('login/',loginView.as_view(),name='login'),
]