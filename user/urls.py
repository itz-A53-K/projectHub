from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('projView/', views.projView, name="projView"),
    path('login/', views.login, name="login"),
    # path('signup/', views.signup, name="signup"),
]
