from django.urls import path
from .views import loginView,logOut,dashBoard,Userprofile

urlpatterns = [
    path('login/',loginView.as_view(),name='login'),
    path('logout/',logOut,name='logout'),
    path('dashboard/',dashBoard,name='dashboard'),
    path('users/',Userprofile.as_view(),name='userprofile'),
]