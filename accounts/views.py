from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate,login
from django.contrib import messages

class loginView(View):

    def get(self,request):
        return render(self.request,'accounts/Login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(self.request,email=email,password=password)
        if user is not None:
            messages.success(self.request,"User Loggined successfully")
            login(self.request,user)
            return render(self.request, 'dashboard.html')
        else:
            messages.error(self.request,"Invalid username or Passowrd")
            return render(self.request, 'accounts/Login.html')


