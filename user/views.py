from user.models import Project, Proj_image, Cart, Order, User_detail
import requests
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.conf import settings
import time
import json

# Define the payment gateway URLs
# PAYU_BASE_URL = 'https://secure.payu.in/_payment'
PAYU_TEST_URL = 'https://test.payu.in/_payment'
PAYU_PRODUCTION_URL = 'https://secure.payu.in/_payment'

# Define the PayU merchant key and salt
# MERCHANT_KEY = 'CY4YAH'
# SALT = '72toOcfuXCBizlYLEGqvVYeIUnXLOGsY'

# Test merchant keys
MERCHANT_KEY = 'gtKFFx'
SALT = '4R38IvwiV57FwVpsgOvTXBdLE4tHUXFW'


def cartCount(user_id):
    cart = Cart.objects.filter(user_id=user_id)
    cart = cart.count()
    return cart


def bought(project, user_id):
    bought = False
    bought = Order.objects.filter(project=project, user_id=user_id).exists()
    return bought


def home(request):
    topProjs = Project.objects.all()[:2]
    params = {'topProjs': topProjs, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/index.html', params)


def projects(request):
    proj = Project.objects.filter(category='Project')
    params = {'proj': proj, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/projects.html', params)


def projView(request, proj_id):
    project = Project.objects.get(proj_id=proj_id)
    images = Proj_image.objects.filter(project=proj_id)
    itemInCart = False
    itemInCart = Cart.objects.filter(
        project=proj_id, user_id=request.user.id).exists()

    params = {'project': project, "cartCount": cartCount(request.user.id),
              "images": images, "itemInCart": itemInCart, 'bought': bought(project, request.user.id)}
    return render(request, 'user/projView.html', params)


def templates(request, data=None):
    if data == None:
        proj = Project.objects.filter(category='Template')
    if data == 'under1k':
        proj = Project.objects.filter(
            Q(category='Template', discounted_price__lte=999))
    elif data == 'over1k':
        proj = Project.objects.filter(
            category='Template', discounted_price__gte=999, free=False)
    elif data == 'free':
        proj = Project.objects.filter(category='Template', free=True)

    params = {'templates': proj, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/templates.html', params)


def tempView(request, temp_id):
    template = Project.objects.get(proj_id=temp_id)
    images = Proj_image.objects.filter(project=temp_id)
    itemInCart = False
    itemInCart = Cart.objects.filter(
        project=temp_id, user_id=request.user.id).exists()

    params = {'template': template, "cartCount": cartCount(
        request.user.id), "images": images, "itemInCart": itemInCart, 'bought': bought(template, request.user.id)}
    return render(request, 'user/projView.html', params)


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
            messages.success(request, "Profile updated successfully.")
            return redirect("/profile/")
        params = {'User_detail': account, "activeProfile": "activeProfile",
                  "cartCount": cartCount(request.user.id)}
        return render(request, "user/profile.html", params)
    else:
        return redirect("/")


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


def handleAddToCart(request, proj_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            proj = Project.objects.get(proj_id=proj_id)
            user_id = request.user.id

            checkBought = bought(proj, user_id)
            if checkBought:
                messages.warning(
                    request, " Seems you already bought this project. Go to 'My Orders' section to download.")
                return JsonResponse({'success': False,
                                     'msg': "", "tag": "danger", "cartCount": cartCount(request.user.id)})
            else:
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


def my_order(request):
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


def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.user.id
            totalprice = request.POST.get('price')

            if totalprice == '0':
                # if item is free
                if cartCount(user_id) == 1:
                    messages.info(
                        request, 'This item is free🎉🥳 for now. You can download it directly.')
                else:
                    messages.info(
                        request, 'This items are free🎉🥳 for now. You can download it directly.')

                cartItems = Cart.objects.filter(user_id=user_id)
                for i in cartItems:
                    cart = Cart.objects.get(project=i.project, user_id=user_id)
                    cart.delete()

                return redirect("/")
            else:
                f_name = request.user.first_name
                email = request.user.email
                phone = User_detail.objects.get(user_id=user_id).phone
                odrItmID = ""

                context = createPayment(
                    totalprice, f_name, email, phone, odrItmID, user_id)
                return render(request, 'user/payment.html', context)
    else:
        messages.error(
            request, "You are not logged in ! Please login first to continue.")
        return redirect("/login")


def buyNow(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.user.id
            proj_id = request.POST.get('proj_id')

            orderedItm = Project.objects.get(proj_id=proj_id)
            checkBought = bought(orderedItm, user_id)
            if checkBought:
                messages.warning(
                    request, " Seems you already bought this project. Go to 'My Orders' section to download.")
                return redirect('/projects')
            else:

                if orderedItm.free:
                    messages.info(
                        request, 'This item is free🎉🥳 for now. You can download it directly.')
                    return redirect('/projects/'+proj_id)

                elif orderedItm.discounted_price is None:
                    price = orderedItm.price

                else:
                    price = orderedItm.discounted_price

                # user detail
                f_name = request.user.first_name
                email = request.user.email
                phone = User_detail.objects.get(user_id=user_id).phone
                odrItmID = orderedItm.proj_id

                context = createPayment(
                    price, f_name, email, phone, odrItmID, user_id)
                return render(request, 'user/payment.html', context)

    else:
        messages.error(
            request, "You are not logged in ! Please login first to continue.")
        return redirect("/login")


# @csrf_exempt
# def paymentSuccess(request):
#     if request.method == "POST":
#         user_id = request.user.id
#         # user_id = request.POST.get('udf2')
#         odrItmID = request.POST.get('udf1')
#         txnID = request.POST.get('txnid')

#         if odrItmID == "":
#             cartItems = Cart.objects.filter(user_id=user_id)
#             for i in cartItems:

#                 if i.project.free:
#                     price = 0
#                 elif i.project.discounted_price:
#                     price = i.project.discounted_price
#                 else:
#                     price = i.project.price

#                 order = Order.objects.create(
#                     project=i.project, user_id=user_id, price=price, transaction_id=txnID)
#                 order.save()
#                 cart = Cart.objects.get(cart_id=i.cart_id)
#                 cart.delete()

#         else:
#             project = Project.objects.get(proj_id=odrItmID)
#             if project.free:
#                 price = 0
#             elif project.discounted_price:
#                 price = project.discounted_price
#             else:
#                 price = project.price

#             price = request.POST.get('amount')
#             order = Order.objects.create(
#                 project=project, user_id=user_id, price=price, transaction_id=txnID)
#             order.save()

#             inCart = False
#             inCart = Cart.objects.filter(
#                 project=project, user_id=user_id).exists()
#             if inCart:
#                 cart = Cart.objects.get(project=project, user_id=user_id)
#                 cart.delete()

#         params = {'success': True, "cartCount": cartCount(user_id)}
#         return render(request, 'user/orderStatus.html', params)


# @csrf_exempt
# def paymentFailed(request):
#     if request.method == "POST":
#         params = {'success': False, "cartCount": cartCount(
#             request.POST.get('udf2'))}
#         return render(request, 'user/orderStatus.html', params)


def generate_hash(params):
    """Function to generate PayU hash"""

    hash_string = ''
    for key in params.keys():
        hash_string += '{}|'.format(params[key])
    hash_string += "||||||||"+SALT

    # print(hash_string)

    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()


def verify_transaction(params):
    """Function to track PayU cash"""

    hash_string = ''
    for key in params.keys():
        hash_string += '{}|'.format(params[key])
    hash_string += SALT
    hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
    print(hash_string)
    print(hash_value)

    url = "https://test.payu.in/merchant/postservice?form=2"
    payload = "key="+MERCHANT_KEY+"&command="+params['command']+"&var1=" + \
        params['var1']+"&hash="+hash_value

    headers = {"Accept": "application/json",
               "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request(
        "POST", url, data=payload, headers=headers, params=params)
    return (response.text)


def createPayment(amount, f_name, email, phone, odrItmID, user_id):  # creating payment for payU
    # Generate the PayU hash
    hash_params = {
        'key': MERCHANT_KEY,
        'txnid': 'TXN{}'.format(time.time()),
        'amount': amount,
        'productinfo': 'Test Product',
        'firstname': f_name,
        'email': email,
        'udf1': odrItmID,
        'udf2': user_id
    }
    # hash value of the above json contents
    hash_params['hash'] = generate_hash(hash_params)

    # Build the PayU payment form fields
    form_data = {
        'key': MERCHANT_KEY,
        'txnid': hash_params['txnid'],
        'amount': hash_params['amount'],
        'productinfo': hash_params['productinfo'],
        'firstname': hash_params['firstname'],
        'email': hash_params['email'],
        'phone': phone,
        # 'surl': 'http://127.0.0.1:8000/paymentSuccess/',
        # 'furl': 'http://127.0.0.1:8000/paymentFailed/',
        'surl': 'http://127.0.0.1:8000/paymentHandler/',
        'furl': 'http://127.0.0.1:8000/paymentHandler/',
        'hash': hash_params['hash'],
        'udf1': hash_params['udf1'],
        'udf2': hash_params['udf2'],
    }

    # payu_url = PAYU_PRODUCTION_URL
    payu_url = PAYU_TEST_URL

    context = {'form_data': form_data, 'payu_url': payu_url}
    return context


@csrf_exempt
def paymentHandler(request):
    if request.method == "POST":
        # user_id = request.user.id
        user_id = request.POST.get('udf2')
        odrItmID = request.POST.get('udf1')
        txnID = request.POST.get('txnid')
        status = request.POST.get('status')
        post_price = request.POST.get('amount')
        net_amount_debit = request.POST.get('net_amount_debit')

        track_params = {
            'key': MERCHANT_KEY,
            # 'command': "verify_payment",
            'command': "get_ws_response",
            'var1': txnID,
        }

        # JSON string
        response = verify_transaction(track_params)
        # deserializes into dict and returns dict.
        dict = json.loads(response)
        # print(dict[response][status])

        # print("JSON string = ", dict)
        # print()
        # print("Status External : "+dict[response][status])

        if status != "success":
            params = {'success': False, "cartCount": cartCount(
                request.POST.get('udf2'))}
            return render(request, 'user/orderStatus.html', params)

        if odrItmID == "":
            cartItems = Cart.objects.filter(user_id=user_id)
            for i in cartItems:

                if i.project.free:
                    price = 0
                elif i.project.discounted_price:
                    price = i.project.discounted_price
                else:
                    price = i.project.price

                print(price)
                order = Order.objects.create(
                    project=i.project, user_id=user_id, price=price, transaction_id=txnID)
                order.save()
                cart = Cart.objects.get(cart_id=i.cart_id)
                cart.delete()
        else:

            project = Project.objects.get(proj_id=odrItmID)
            if project.free:
                price = 0
            elif project.discounted_price:
                price = project.discounted_price
            else:
                price = project.price

            print(price)
            #  or price != post_price or net_amount_debit != price
            if status != "success":
                params = {'success': False, "cartCount": cartCount(
                    request.POST.get('udf2'))}
                return render(request, 'user/orderStatus.html', params)
            else:
                order = Order.objects.create(
                    project=project, user_id=user_id, price=price, transaction_id=txnID)
                order.save()

                inCart = False
                inCart = Cart.objects.filter(
                    project=project, user_id=user_id).exists()
                if inCart:
                    cart = Cart.objects.get(project=project, user_id=user_id)
                    cart.delete()

        params = {'success': True, "cartCount": cartCount(user_id)}
        return render(request, 'user/orderStatus.html', params)
        # return HttpResponse("gada")
    else:
        params = {'success': False, "cartCount": cartCount(
            request.POST.get('udf2'))}
        return render(request, 'user/orderStatus.html', params)
