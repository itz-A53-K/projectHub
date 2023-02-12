from django.shortcuts import render,HttpResponse, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'user/index.html')

def projView(request):
    return render(request, 'user/projView.html')

def login(request):
    if request.method == "POST":
        form = request.POST.get('formType')
        if form == "login" :
            email = request.POST.get('email','')
            password = request.POST.get('upass','')
            print(email,password)
            user = authenticate(username=email,password =password)

            if user is not None:
                # login(user)
                messages.success(request, "You have loggedin successfully")
                return redirect('/')
                
            else:
                # print('Invalid username')
                messages.warning(request, "Error! Invalid username or password")
       
        elif form =="registration" :
            # Database Insertion Here
            email_reg = request.POST.get('email_reg')
            password = request.POST.get('password')
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            # print(form)

            try:
                user= User.objects.create_user(username=email_reg, email=email_reg, password=password)
                user.first_name= f_name
                user.last_name= l_name
                user.save()
                messages.success(request,"Your account has been successfully created")
                return redirect('/')
            except:
                messages.warning(request,"Email already exists")
            
            
    return render(request, 'user/login.html')

