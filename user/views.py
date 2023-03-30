from user.models import Project, Proj_image, Cart, Order, User_detail
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from django.core.mail import send_mail

import requests
import random
import hashlib
import time
import json
import os

BASE = 'https://www.projectcodes.online'
# BASE = 'http://127.0.0.1:8000'

# Define the payment gateway URLs
# PAYU_TEST_URL = 'https://test.payu.in/_payment'
PAYU_PRODUCTION_URL = 'https://secure.payu.in/_payment'

# PayU Production merchant key and salt
MERCHANT_KEY = 'CY4YAH'
SALT = '72toOcfuXCBizlYLEGqvVYeIUnXLOGsY'

# PayU Test merchant keys
# MERCHANT_KEY = 'gtKFFx'
# SALT = '4R38IvwiV57FwVpsgOvTXBdLE4tHUXFW'


def cartCount(user_id):
    cart = Cart.objects.filter(user_id=user_id)
    cart = cart.count()
    return cart


def bought(project, user_id):
    bought = False
    bought = Order.objects.filter(project=project, user_id=user_id).exists()
    return bought


def home(request):
    topProjs = Project.objects.filter(category='Project')[:1]
    topTemps = Project.objects.filter(category='Template')[:1]
    params = {'topProjs': topProjs, 'topTemps': topTemps,
              "cartCount": cartCount(request.user.id)}
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

    params = {'templates': proj, "cartCount": cartCount(
        request.user.id)}
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
                messages.error(
                    request, "Error! Invalid username or password")
                return redirect("/login")

        elif form == "registration":
            inp_otp= request.POST.get('input_otp')
            generated_otp = request.session['regi_generated_OTP']

            email_reg = request.POST.get('email')
            session_email = request.session['session_email']

            if int(inp_otp) == generated_otp and email_reg == session_email:
                password = request.POST.get('password')
                f_name = request.POST.get('f_name')
                l_name = request.POST.get('l_name')
                try:
                    #deleting sessions
                    del request.session['regi_generated_OTP']
                    del request.session['session_email']
                except:
                    print("session can't be deleted")

                try:
                    user = User.objects.create_user( username=email_reg, email=email_reg, password=password)
                    user.first_name = f_name
                    user.last_name = l_name
                    user.save()

                    user = User.objects.get(username=email_reg)
                    name = user.first_name+" " + user.last_name
                    account = User_detail.objects.create( user_id=user.id, name=name)
                    account.save()
                    messages.success(
                        request, "Your account has been successfully created. You can login now.")
                    return JsonResponse({'success': True})
                except:
                    messages.error(request, "Email already exists.")
                    return JsonResponse({'success': False})
            else:
                return JsonResponse({'success': False, 'msg': 'Invalid OTP'})

    elif request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            #deleting sessions
            del request.session['regi_generated_OTP']
            del request.session['session_email']
        except:
            print("session can't be deleted")

        return render(request, 'user/login.html')


def sendOtp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(username=email, email=email).exists()
        if user:
            messages.success(request, "You are already registered. Please login.")
            return JsonResponse({'msg': "Email already exist", 'success': False, 'errorTyoe': "email"})
        else:
            otp= random.randint(100000 ,999999)
            msg= f'''Hello Dear,

    Thank you for signing in with Projectcodes.online. We want to make sure it's really you. Your One-Time Password (OTP) to complete the registration process is {otp} (Valid only for 5 minutes). Please do not share the OTP with anyone.
    If you don't want to create an account, you can ignore this message. 

    Thank you,
    Team Projectcodes.online                       
   '''
            
            send_mail(
                'Projectcodes.online Email Verification',
                msg,
                'projectzcodes@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['regi_generated_OTP'] = otp
            request.session['session_email'] = email
            return JsonResponse({'success': True, 'msg': 'Varification code sent to', 'email' : email})
    else:
        return redirect("/")


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

    if request.method =="GET":
        project_id= request.GET.get("id")
        project = Project.objects.get(proj_id= project_id)
        order = Order.objects.filter(project=project, user_id=request.user.id).exists()

        if project.free or order:
            source = os.path.dirname(os.path.dirname(__file__)) + '/media/projectFile/' + project.sourcecode_link
            return serve(request, os.path.basename(source), os.path.dirname(source))
        else:
            messages.error(request , "We are sorry. This item is no longer available for free.")
            if project.category == "Project":
                redirect_url= "/projects/"+project_id
            else:
                redirect_url= "/templates/view/"+project_id

            return redirect(redirect_url)
    else:
        return redirect('/')

# not gonna use the following method for now because of bad user experiance as gplink shows too long add
 
    # if request.user.is_authenticated and request.method == "GET":
    #     project_id = request.GET.get("id")
    #     project = Project.objects.get(proj_id=project_id)

    #     if not project.free:
    #         order = Order.objects.filter(project=project, user_id=request.user.id).exists()

    #         if order:
    #             source = os.path.dirname(os.path.dirname(
    #                 __file__)) + '/media/projectFile/' + project.sourcecode_link
    #             return serve(request, os.path.basename(source), os.path.dirname(source))
    #         else:
    #             raise Http404('Order do not exists.')
    #     else:
    #         headers = {"Accept": "application/json",
    #                    "Content-Type": "application/x-www-form-urlencoded"}
    #         # alias = "Source_"+randint(1, 10909900)
    #         api_url = "https://gplinks.in/api?api=717ef637312487810f5a0efe2d80b127115c0b6a&url=" + BASE + \
    #             "/ad_viewed/?id=" + project_id + "&alias=" + \
    #             'Source_Code_{}'.format(random.randint(1, 10909900377777))
    #         # print(api_url)
    #         response = requests.request(
    #             "GET", api_url)
    #         # print(response.text)
    #         dict = json.loads(response.text)
    #         if dict['status'] == "success":
    #             return redirect(dict["shortenedUrl"])
    #         else:
    #             return redirect("/")


def ad_viewed(request):
    # if request.user.is_authenticated and request.method == "GET":
    #     project_id = request.GET.get("id")
    #     project = Project.objects.get(proj_id=project_id)

    #     if project.free:
    #         source = os.path.dirname(os.path.dirname(
    #             __file__)) + '/media/projectFile/' + project.sourcecode_link
    #         return serve(request, os.path.basename(source), os.path.dirname(source))
    #     else:
    #         return redirect("/")
    return HttpResponse('Ad Viewed')


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


def generate_hash(params):
    """Function to generate PayU hash"""

    hash_string = ''
    for key in params.keys():
        hash_string += '{}|'.format(params[key])
    hash_string += "||||||||"+SALT
    # print(hash_string)

    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()


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
        'surl': BASE+'/payment/',
        'furl': BASE+'/payment/',
        'hash': hash_params['hash'],
        'udf1': hash_params['udf1'],
        'udf2': hash_params['udf2'],
    }

    payu_url = PAYU_PRODUCTION_URL
    # payu_url = PAYU_TEST_URL

    context = {'form_data': form_data, 'payu_url': payu_url}
    return context


@csrf_exempt
def payment(request):
    if request.method == "POST":
        # user_id = request.user.id
        user_id = request.POST.get('udf2')
        odrItmID = request.POST.get('udf1')
        txnID = request.POST.get('txnid')
        status = request.POST.get('status')
        # post_price = request.POST.get('amount')
        # net_amount_debit = request.POST.get('net_amount_debit')

        track_params = {
            'key': MERCHANT_KEY,
            # 'command': "verify_payment",
            'command': "get_ws_response",
            'var1': txnID,
        }

        pauyResponse = verify_transaction(track_params)
        # print(pauyResponse)
        dict = json.loads(pauyResponse)
        # print(dict['response']['status'])

        if dict['response']['status'] != "success":
            return redirect('/orderfailed')

        else:
            if dict['response']['status'] == "success" and status == "success":
                if odrItmID == "":
                    # if order request is sent from cart (checkout button)
                    cartItems = Cart.objects.filter(user_id=user_id)
                    for i in cartItems:

                        if i.project.free:
                            price = 0
                        elif i.project.discounted_price:
                            price = i.project.discounted_price
                        else:
                            price = i.project.price

                        order = Order.objects.create(
                            project=i.project, user_id=user_id, price=price, transaction_id=txnID)
                        order.save()
                        cart = Cart.objects.get(cart_id=i.cart_id)
                        cart.delete()
                else:
                    # if order request is sent through buyNow button
                    project = Project.objects.get(proj_id=odrItmID)
                    if project.free:
                        price = 0
                    elif project.discounted_price:
                        price = project.discounted_price
                    else:
                        price = project.price

                    order = Order.objects.create(
                        project=project, user_id=user_id, price=price, transaction_id=txnID)
                    order.save()

                    inCart = False
                    inCart = Cart.objects.filter(
                        project=project, user_id=user_id).exists()
                    if inCart:
                        cart = Cart.objects.get(
                            project=project, user_id=user_id)
                        cart.delete()
                return redirect('/ordersuccess')
            else:
                return redirect('/orderfailed')

        # return HttpResponse("gada")
    else:
        return redirect('/orderFailed')


def verify_transaction(params):
    """Function to track PayU cash"""

    hash_string = ''
    for key in params.keys():
        hash_string += '{}|'.format(params[key])
    hash_string += SALT
    hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

    url = "https://info.payu.in/merchant/postservice?form=2"
    payload = "key="+MERCHANT_KEY+"&command="+params['command']+"&var1=" + \
        params['var1']+"&hash="+hash_value

    headers = {"Accept": "application/json",
               "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request(
        "POST", url, data=payload, headers=headers, params=params)
    return (response.text)


def ordersuccess(request):
    params = {'success': True, "cartCount": cartCount(request.user.id)}
    return render(request, 'user/orderStatus.html', params)


def orderfailed(request):
    params = {'success': False, "cartCount": cartCount(
        request.POST.get('udf2'))}
    return render(request, 'user/orderStatus.html', params)


def resetPass(request):
    if request.method=="POST" :
        if not request.user.is_authenticated:
            newPass= request.POST.get('newPass')

            inputOTP= request.POST.get('inputOTP')
            resetpass_generated_OTP = request.session['resetpass_generated_OTP']

            inputEmail = request.POST.get('inputEmail')
            resetpass_email = request.session['resetpass_email']
            if int(inputOTP) == resetpass_generated_OTP and inputEmail== resetpass_email:
                try:
                    user= User.objects.get(username= inputEmail, email= inputEmail)
                    print(newPass)
                    user.set_password(newPass)
                    user.save()
                    print("pr "+user.password)
                    try:
                        del request.session['resetpass_generated_OTP']
                        del request.session['resetpass_email']
                        print("session deleted")
                    except Exception as e:
                        print(e)
                    
                    messages.success(request, 'Password has been changed successfully.' )
                    return JsonResponse({'success': True, 'msg': 'Password has been changed successfully.'})
                except:
                    messages.error(request, 'Internel error. Password can not be changed.' )
                    return JsonResponse({'success': False, 'msg': 'Internel error. Password can not be changed.'})
            else:
                return JsonResponse({'success': False, 'msg': 'Hacked'})

        else:
            messages.error(request, 'Insecure request !' )
            return redirect('/')
    else:
        return render(request, "user/resetPass.html")



def resetPass_SandOTP(request):
    if request.method=="POST" :
        if not request.user.is_authenticated:
            inp_email= request.POST.get('inputEmail')
            user = User.objects.filter(username=inp_email, email=inp_email).exists()
            if user:
            
                reset_otp= random.randint(100000 ,999999)
                reset_msg= f'''Hello Dear,

    We received a request to reset your account password. Your One-Time Password (OTP) to complete the reset password process is {reset_otp} (Valid only for 5 minutes). Please do not share the OTP with anyone.
    If you did not initiate this request, you can ignore this message.
    
    Thank you,
    Team Projectcodes.online'''  
                              
                send_mail(
                    'Projectcodes.online Reset Password',
                    reset_msg,
                    'projectzcodes@gmail.com',
                    [inp_email],
                    fail_silently=False,
                )
                request.session['resetpass_generated_OTP']= reset_otp
                request.session['resetpass_email']=inp_email
                
                return JsonResponse({ 'msg': f'An Email with a verification code sent to your email address "{inp_email}"','success': True})
            else:
                messages.success(request, "No account found.")
                return JsonResponse({'msg': f'No account found with the email "{inp_email}".', 'success': False})
    else:
        
        return redirect('/')

def resetPass_verifyOTP(request):
    if request.method=="POST":
        if not request.user.is_authenticated:

            inputOTP= request.POST.get('inputOTP')
            resetpass_generated_OTP = request.session['resetpass_generated_OTP']

            inputEmail = request.POST.get('inputEmail')
            resetpass_email = request.session['resetpass_email']
            if int(inputOTP) == resetpass_generated_OTP and inputEmail== resetpass_email:
                
                return JsonResponse({'success': True, 'msg': 'OTP verify success.'})
            else:
                return JsonResponse({'success': False, 'msg': 'OTP do not match. Please enter valid OTP.'})
    else:
        return redirect('/')
    # else:
    #     return render(request, "user/resetPass.html")

    