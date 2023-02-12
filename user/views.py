from django.shortcuts import render,HttpResponse

def home(request):
    return render(request, 'user/index.html')

def projView(request):
    return render(request, 'user/projView.html')

def login(request):
    if request.method == "POST":
        form = request.POST.get('formType')
        if form == "login" :
            print(form)
            # Database Insertion Here
        else :
            print(form)
            # Database Insertion Here

    return render(request, 'user/login.html')

