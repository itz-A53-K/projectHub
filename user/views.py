from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from user.form import ImageForm

from django.db.models import Q

from user.models import Project,Proj_image,Cart,Order,User_detail

def cartCount(user_id):
    cart= Cart.objects.filter(user_id = user_id)
    cart= cart.count()
    return cart

def home(request):
    topProjs= Project.objects.all()[:2]
    params={'topProjs':topProjs, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/index.html', params)

def projects(request):
    proj= Project.objects.all()
    params={'proj': proj, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/projects.html', params)

def projView(request, proj_id):
    project= Project.objects.get(proj_id = proj_id)
    images=Proj_image.objects.filter(proj_id=proj_id)
    params={'project': project, "cartCount": cartCount(request.user.id), "images":images}
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
                messages.success(request,"Your account has been successfully created. You can login now.")
                return redirect('/login/')
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


def profile(request):
    if request.user.is_authenticated:
        user_id= request.user.id
        account= User_detail.objects.get(user_id= user_id)
        
        if request.method=="POST":
            f_name=request.POST.get('f_name')
            l_name=request.POST.get('l_name')
            gender=request.POST.get('gender')
            phone=request.POST.get('phone')
            address=request.POST.get('address')
            profileImg=request.POST.get('profileImg')
        
            user= User.objects.get(id=user_id)
            user.first_name=f_name
            user.last_name= l_name

            account.gender=gender
            account.phone=phone
            account.address=address
            # account.profileImg=profileImg
            account.save()
            user.save()
            return redirect("/profile/")
        params={'User_detail' : account, "activeProfile" : "activeProfile", "cartCount": cartCount(request.user.id)}
        return render(request, "user/profile.html", params)
    else:
        return redirect("/")
    

def order(request):
    if request.user.is_authenticated:
        user_id= request.user.id
        account= User_detail.objects.get(user_id= user_id)
        # order= Order.objects.get(user_id= user_id)
        # print(order)
        
        params={'User_detail' : account, "activeOrder" : "activeOrder", "orders": "order", "cartCount": cartCount(request.user.id)}
        return render(request, "user/profile.html", params)
    else:
        return redirect("/")
    

    
def handleAddToCart(request, proj_id):
    if request.method =='POST':
        if request.user.is_authenticated:
            proj = Project.objects.get(proj_id=proj_id)
            
            user_id= request.user.id
            
            itemInCart= Cart.objects.filter(project= proj, user_id=user_id)
            if not itemInCart.count() is 0:
                return JsonResponse({'success': True,
                         'msg': "Unable to add! Item already in cart.", "tag": "danger"
                         , "cartCount": cartCount(request.user.id)})
            else:
                cart= Cart.objects.create(project = proj,user_id = user_id)
                cart.save()
                return JsonResponse({'success': True,
                         'msg': "Item added to cart successfully.", "tag": "success"
                         , "cartCount": cartCount(request.user.id)})
            # messages.success(request, "1 Item added to cart successfully.")
        else:
            # messages.error(request, "Please Login First To Continue")
            return JsonResponse({'success': False,
                         'msg': "Please Login First To Continue", "tag": "danger"
                         , "cartCount": cartCount(request.user.id)})
    else :
        return redirect('/projects/')



def cart(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        cart= Cart.objects.filter(user_id=user_id)
        total_original_price = 0
        total_descounted_price = 0
        for i in cart:
            total_original_price += i.project.price

            if i.project.free :
                price = 0
            elif i.project.discounted_price :
                price = i.project.discounted_price
            else :
                price = i.project.price

            total_descounted_price += price

        # print(total_descounted_price)
        discount= total_original_price-total_descounted_price

        params={"cart": cart, "cartCount": cartCount(user_id), "total_original_price" : total_original_price, "total_descounted_price": total_descounted_price, "discount": discount}
        return render(request,"user/cart.html", params)
    else :
        return redirect('/')
    


def search(request):
    if request.method=="GET":
        src_query=request.GET.get("src_query")
        print(src_query)
        srcResult=Project.objects.filter(Q(title__icontains=src_query) |Q(short_Desc__icontains=src_query)| Q(full_Desc__icontains=src_query) )
        
        params={"srcResult": srcResult, "src": "true", "src_query":src_query}
        return render(request, "user/projects.html", params)
    else:
        return redirect("/")
    


def removeFromCart(request , cart_id):
    if request.user.is_authenticated:
        # cart_id= cart_id
        cart= Cart.objects.filter(cart_id= cart_id)
        cart.delete()
        
        return redirect("/cart/")
    else:
        return redirect("/")
