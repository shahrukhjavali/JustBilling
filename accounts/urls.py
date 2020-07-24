from django.urls import path
from .views import loginView,logOut,dashBoard

urlpatterns = [
    path('login/',loginView.as_view(),name='login'),
    path('logout/',logOut,name='logout'),
    path('dashboard/',dashBoard,name='dashboard'),
]