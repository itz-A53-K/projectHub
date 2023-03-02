from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from user.form import ImageForm
from django.db.models import Q
import hashlib

from user.models import Project, Proj_image, Cart, Order, User_detail


def cartCount(user_id):
    cart = Cart.objects.filter(user_id=user_id)
    cart = cart.count()
    return cart


def home(request):
    topProjs = Project.objects.all()[:2]
    params = {'topProjs': topProjs, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/index.html', params)


def projects(request):
    proj = Project.objects.all()
    params = {'proj': proj, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/projects.html', params)


def projView(request, proj_id):
    project = Project.objects.get(proj_id=proj_id)
    images = Proj_image.objects.filter(project=proj_id)
    itemInCart = False
    itemInCart = Cart.objects.filter(
        project=proj_id, user_id=request.user.id).exists()

    params = {'project': project, "cartCount": cartCount(
        request.user.id), "images": images, "itemInCart": itemInCart}
    return render(request, 'user/projView.html', params)


def handleLogin(request):
    if request.method == "POST":

        form = request.POST.get('formType')
        if form == "login":
            email = request.POST.get('email', '')
            password = request.POST.get('upass', '')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have loggedin successfully")
                return redirect('/')

            else:
                messages.error(request, "Error! Invalid username or password")

        elif form == "registration":
            email_reg = request.POST.get('email_reg')
            password = request.POST.get('password')
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')

            try:
                user = User.objects.create_user(
                    username=email_reg, email=email_reg, password=password)
                user.first_name = f_name
                user.last_name = l_name
                user.save()
                user = User.objects.get(username=email_reg)
                name = user.first_name+" " + user.last_name
                account = User_detail.objects.create(
                    user_id=user.id, name=name)
                account.save()
                messages.success(
                    request, "Your account has been successfully created. You can login now.")
                return redirect('/login/')
            except:
                messages.error(request, "Error! Email already exists.")

    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'user/login.html')


def handleLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have logged out successfully.")
        return redirect('/')
    else:
        return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        account = User_detail.objects.get(user_id=user_id)

        if request.method == "POST":
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            profileImg = request.POST.get('profileImg')

            user = User.objects.get(id=user_id)
            user.first_name = f_name
            user.last_name = l_name

            account.gender = gender
            account.phone = phone
            account.address = address

            account.save()
            user.save()
            return redirect("/profile/")
        params = {'User_detail': account, "activeProfile": "activeProfile",
                  "cartCount": cartCount(request.user.id)}
        return render(request, "user/profile.html", params)
    else:
        return redirect("/")


def handleAddToCart(request, proj_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            proj = Project.objects.get(proj_id=proj_id)
            user_id = request.user.id

            cart = Cart.objects.create(project=proj, user_id=user_id)
            cart.save()
            messages.success(request, " Item added to cart successfully.")
            return JsonResponse({'success': True,
                                 'msg': "", "tag": "success", "cartCount": cartCount(request.user.id)})
        else:
            messages.error(request, "Please Login First To Continue")
            return JsonResponse({'success': False,
                                 'msg': "", "tag": "danger", "cartCount": cartCount(request.user.id)})
    else:
        return redirect('/projects/')


def cart(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        cart = Cart.objects.filter(user_id=user_id).order_by('-cart_id')

        total_original_price = 0
        total_descounted_price = 0
        for i in cart:
            total_original_price += i.project.price

            if i.project.free:
                price = 0
            elif i.project.discounted_price:
                price = i.project.discounted_price
            else:
                price = i.project.price

            total_descounted_price += price

        discount = total_original_price-total_descounted_price

        params = {"cart": cart, "cartCount": cartCount(
            user_id), "total_original_price": total_original_price, "total_descounted_price": total_descounted_price, "discount": discount}
        return render(request, "user/cart.html", params)
    else:
        return redirect('/')


def search(request):
    if request.method == "GET":
        src_query = request.GET.get("src_query")

        srcResult = Project.objects.filter(Q(title__icontains=src_query) | Q(
            short_Desc__icontains=src_query) | Q(full_Desc__icontains=src_query))

        params = {"srcResult": srcResult,
                  "src": "true", "src_query": src_query}
        return render(request, "user/projects.html", params)
    else:
        return redirect("/")


def removeFromCart(request, cart_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(cart_id=cart_id)
        for i in cart:
            title = i.project.title
        cart.delete()
        messages.success(request, "Successfully removed '" +
                         title + "' from your cart !")
        return redirect("/cart/")
    else:
        return redirect("/")


def buy(request, proj_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        proj_id = proj_id

        PAYU_BASE_URL = "https://secure.payu.in/_payment"
        action = ''
        posted = {}
        token = ""
        SALT = "72toOcfuXCBizlYLEGqvVYeIUnXLOGsY"
        hash_object = hashlib.sha256(token.encode('utf-8'))
        print(token)
        txnid = hash_object.hexdigest()[0:20]
        hashh = ''
        print('Came here')
        posted['key'] = "CY4YAH"
        posted['txnid'] = txnid
        posted['amount'] = 234
        posted['productinfo'] = "None"
        posted['firstname'] = "Nishal"
        posted['phone'] = "9101114906"
        posted['email'] = "nishalbarman@gmail.com"
        posted['surl'] = 'http://127.0.0.1:8000/success/'
        print(posted['surl'])
        posted['furl'] = 'http://127.0.0.1:8000/fail/'
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string += str(posted[i])
            except Exception:
                hash_string += ''
                hash_string += '|'
                hash_string += SALT
                # print(hash_string)
                hashh = hashlib.sha512(
                    hash_string.encode('utf-8')).hexdigest().lower()
        action = 'https://secure.payu.in/_payment'
        print(hashh)
        params = "all bll"
        return render(request, "user/checkout.html", params)
    else:
        messages.error(
            request, "You are not logged in ! Please login first to continue.")
        return redirect("/login")


def order(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        account = User_detail.objects.get(user_id=user_id)
        orders = Order.objects.filter(user_id=user_id).order_by('-order_id')
        params = {'User_detail': account, "activeOrder": "activeOrder",
                  "orders": orders, "cartCount": cartCount(user_id)}
        return render(request, "user/profile.html", params)
    else:
        return redirect("/")


def download(request):
    if request.user.is_authenticated and request.method == "POST":
        order_id = request.POST.get("ord_id")
        print(order_id)
        order = Order.objects.get(order_id=order_id, user_id=request.user.id)
        return HttpResponse("njhfkjdhfh")
