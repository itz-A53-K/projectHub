from django import forms
from user.models import User_detail

class ImageForm(forms.ModelForm) :
    class Meta: 
        model=User_detail
        fields=("id", "user_id", "name", "gender", "phone", "address", "profileImg")