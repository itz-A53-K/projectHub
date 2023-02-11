from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request, 'user/index.html')

def projView(request):
    return render(request, 'user/projView.html')

def login(request):
    return render(request, 'user/login.html')

def signup(request):
    return render(request, 'user/signup.html')