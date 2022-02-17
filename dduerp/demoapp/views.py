import imp
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User as us
from django.contrib.auth.models import User, auth

# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['id']
        password=request.POST['pass']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'home.html')
        else:
            messages.info(request,'user not exist')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method=='POST':
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pwd1=request.POST['pwd1']
        pwd2=request.POST['pwd2']
        if pwd1 == pwd2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'user exist')
                return render(request,'signup.html')
            else:
                user = User.objects.create_user(username=email, password=pwd1,first_name=fname,last_name=lname)
                user.save()
                # auth.login(request,user)
                return render(request, 'login.html')
        else:
            messages.info(request,'password not matching')
            return render(request,'signup.html')

    else:
        return render(request,'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('home')