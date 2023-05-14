from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Item, Size, Stock, Purchase, User

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class SalesForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    size = forms.ModelChoiceField(queryset=Size.objects.all())
    quantity = forms.IntegerField()


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'


class LoginForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser', 'password1', 'password2')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')