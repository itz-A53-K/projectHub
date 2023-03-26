from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from user.models import Project, Proj_image, Cart, Order, User_detail

# Register your models here.
@admin.register(Project)
class projectModel(admin.ModelAdmin):
    list_display= ["title","price", "discounted_price", "free"]



# admin.site.register(Proj_image)
@admin.register(Proj_image)
class projectImgModel(admin.ModelAdmin):
    list_display= ["id","proj_info","image_url"]

    def proj_info(self,obj):
        link= reverse("admin:user_project_change", args=[obj.project.proj_id])
        return format_html('<a href="{}">{}</a>', link, obj.project)



@admin.register(Cart)
class CartModel(admin.ModelAdmin):
    # list_display= ["order_id","project","projectInfo" ,"user_id","transaction_id"]
    list_display= ["cart_id","project_info","user_id"]
    
    def project_info(self,obj):
        link= reverse("admin:user_project_change", args=[obj.project.proj_id])
        return format_html('<a href="{}">{}</a>', link, obj.project.title)
    
    def user_info(self,obj):
        link= reverse("admin:user_user_detail_change", args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', link, obj.user_id)



@admin.register(Order)
class orderModel(admin.ModelAdmin):
    # list_display= ["order_id","project","projectInfo" ,"user_id","transaction_id"]
    list_display= ["order_id","project_info" ,"user_id","transaction_id"]
    
    def project_info(self,obj):
        link= reverse("admin:user_project_change", args=[obj.project.proj_id])
        return format_html('<a href="{}">{}</a>', link, obj.project.title)
    
    # def transaction_info(self,obj):
        # link= reverse("admin:user_transaction_change", args=[obj.id])
        # return format_html('<a href="{}">{}</a>', link, obj.transaction_id)



@admin.register(User_detail)
class User_detailModel(admin.ModelAdmin):
    list_display= ["name","id","user_id" ]
   
