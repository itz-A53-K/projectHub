from django.contrib import admin
from user.models import Project, Proj_image, Cart, Order, User_detail

# Register your models here.
admin.site.register(Project)
admin.site.register(Proj_image)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(User_detail)
