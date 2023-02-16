from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

from user.models import Project,Proj_image,Cart,Order,User_detail

def home(request):
    topProjs= Project.objects.all()[:2]
    params={'topProjs':topProjs}
    return render(request, 'user/index.html', params)

def projects(request):
    proj= Project.objects.all()
    params={'proj': proj}
    return render(request, 'user/projects.html', params)

def projView(request, proj_id):
    project= Project.objects.get(proj_id = proj_id)
    print(project)
    print(project.short_Desc)
    params={'project': project}
    return render(request, 'user/projView.html' , params)

def handleLogin(request):
    if request.method == "POST" :
       
        form = request.POST.get('formType')
        if form == "login" :
            email = request.POST.get('email','')
            password = request.POST.get('upass','')
            print(email,password)
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have loggedin successfully")
                return redirect('/')
                
            else:
                # print('Invalid username')
                messages.error(request, "Error! Invalid username or password")

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
                user=User.objects.get(username=email_reg)
                # print(u1.id)
                name= user.first_name+" "+ user.last_name
                account= User_detail.objects.create(user_id= user.id, name= name)
                account.save()
                messages.success(request,"Your account has been successfully created.")
                return redirect('/')
            except:
                messages.error(request,"Error! Email already exists.")

    if request.user.is_authenticated:
        return redirect('/')
    else:  
        return render(request, 'user/login.html')


def handleLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"You have logged out successfully.")
        return redirect('/')
    else:
        return redirect('/')


def handleAddToCart(request, proj_id):
    if request.method =='POST':
        if request.user.is_authenticated:
            proj = Project.objects.get(proj_id= proj_id)
            user_id= request.user.id
            price = request.POST.get("price")
            cart= Cart.objects.create(project = proj,user_id = user_id, price =price)
            cart.save()
            # messages.success(request, "1 Item added to cart successfully.")
            return JsonResponse({'success': True,
                         'msg': "Item added to cart successfully.", "tag": "success"})
        else:
            # messages.error(request, "Please Login First To Continue")
            return JsonResponse({'success': False,
                         'msg': "Please Login First To Continue", "tag": "danger"})
    else :
        return redirect('/projects/')

def profile(request):
    if request.user.is_authenticated:
        user_id= request.user.id
        account= User_detail.objects.get(user_id= user_id)
        if request.method=="POST":
            f_name=request.POST.get('f_name')
            l_name=request.POST.get('l_name')
            gender=request.POST.get('gender')
            phone=request.POST.get('phone')
            profileImg=request.POST.get('profileImg')
            
            user= User.objects.get(id=user_id)
            user.first_name=f_name
            user.last_name= l_name

            account.gender=gender
            account.phone=phone
            account.profileImg=profileImg
            # account.price="100"
            account.save()
            user.save()
            return redirect("/profile/")
        params={'User_detail' : account}
        return render(request, "user/profile.html", params)
    else:
        return redirect("/")