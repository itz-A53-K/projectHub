from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('projects/', views.projects, name="projects"),
    path('projects/<proj_id>', views.projView, name="projView"),

    path('templates/', views.templates, name="templates"),
    path('templates/<slug:data>', views.templates, name="filteredTemplates"),
    path('templates/view/<temp_id>', views.tempView, name="tempView"),

    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('profile/', views.profile, name="profile"),

    path('cart/', views.cart, name="cart"),
    path('handleAddToCart/<proj_id>',
         views.handleAddToCart, name="handleAddToCart"),
    path('remove/<cart_id>', views.removeFromCart, name="removeFromCart"),

    path('search/', views.search, name="search"),

    path('checkout/', views.checkout, name="checkout"),
    path('buy/', views.buyNow, name="buyNow"),
    #     path('handelPaymentRequest/', views.handelPaymentRequest,name="handelPaymentRequest"),

    # path('paymentSuccess/', views.paymentSuccess, name="paymentSuccess"),
    # path('paymentFailed/', views.paymentFailed, name="paymentFailed"),
    path('paymentHandler/', views.paymentHandler, name="paymentHandler"),

    path('order/', views.my_order, name="order"),

    path('download/', views.download, name="download"),
    # path('create-paypal-order/', views.createPaypalOrder, name="createPaypalOrder"),
]
