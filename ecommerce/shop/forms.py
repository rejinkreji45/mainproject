from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1','password2', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from shop.models import Category,Product
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','description','price','image','stock','category']


class StockForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['stock']