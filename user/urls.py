from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('projects/', views.projects, name="projects"),
    path('projects/<proj_id>', views.projView, name="projView"),
    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('profile/', views.profile, name="profile"),
    path('order/', views.order, name="order"),
    path('cart/', views.cart, name="cart"),
    path('handleAddToCart/<proj_id>', views.handleAddToCart, name="handleAddToCart"),
]
