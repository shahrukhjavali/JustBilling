from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from products.models import Products
from django.contrib.auth.decorators import login_required

class loginView(View):

    def get(self,request):
        return render(self.request,'accounts/Login.html')

    def post(self,request):
        object_count = Products.objects.all().count()
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(self.request,email=email,password=password)
        if user is not None:
            messages.success(self.request,"User Loggined successfully")
            login(self.request,user)
            return render(self.request, 'dashboard.html',{'product_count':object_count})
        else:
            messages.error(self.request,"Invalid username or Passowrd")
            return render(self.request, 'accounts/Login.html')

def logOut(request):
    logout(request)
    return redirect('/login')

@login_required
def dashBoard(request):
    object_count = Products.objects.all().count()
    return render(request, 'dashboard.html',{'product_count':object_count})
