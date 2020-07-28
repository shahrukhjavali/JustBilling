from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from products.models import Products
from accounts.models import User
from billing.models import Customer
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


class loginView(View):

    def get(self, request):
        return render(self.request, 'accounts/Login.html')

    def post(self, request):
        object_count = Products.objects.all().count()
        custcount = Customer.objects.count()
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            messages.success(self.request, "User Loggined successfully")
            login(self.request, user)
            return render(self.request, 'dashboard.html', {'product_count': object_count,'customercount':custcount})
        else:
            messages.error(self.request, "Invalid username or Passowrd")
            return render(self.request, 'accounts/Login.html')


def logOut(request):
    logout(request)
    return redirect('/login')

class Userprofile(View):
    def get(self, request):
        allusers = User.objects.all().order_by('-id')
        paginator = Paginator(allusers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request,'user/users.html', {'user_all': page_obj})

    def post(self,request):
        email = str(request.POST.get('email'))
        #confirmpass = request.POST.get('confirmpassword')
        password = request.POST.get('password')
        print(password)
        user = User.objects.create_superuser(self,password,email)
        allusers = User.objects.all().order_by('-id')
        paginator = Paginator(allusers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'user/users.html', {'user_all': page_obj})

@login_required
def dashBoard(request):
    object_count = Products.objects.all().count()
    return render(request, 'dashboard.html', {'product_count': object_count})



