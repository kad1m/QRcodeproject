from django import forms
from .models import Website, CafeMenu, Category, Product, Customer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _


class CreateQrCodeForm(forms.ModelForm):

    class Meta:
        model = Website
        fields = ('name',)

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': _('Your name'), 'name': 'message-name'}))


class CreateQrCodeForMenuForm(forms.ModelForm):

    class Meta:
        model = CafeMenu
        fields = ('name', 'menu_pdf')

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': 'Your li', 'name': 'message-name'}))


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', 'description')

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': _('Category name'), 'name': 'message-name'}))
    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': _('Description'), 'name': 'message-name'}))


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'product_image')

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': _('Product name'), 'name': 'message-name'}))

    price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': _('Price'), 'name': 'message-name'}))

    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': _('Description'), 'name': 'message-name'}))


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username'), 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
            'id': 'hi',
        }
    ))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username'), 'id': 'hello'}), help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'hi',
        }
    ), help_text=[_('Your password can’t be too similar to your other personal information.'),
                   _('Your password must contain at least 8 characters.'),
                   _('Your password can’t be a commonly used password.'),
                   _('Your password can’t be entirely numeric.')])
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Confirm password'),
            'id': 'hi',

        }
    ), help_text=_('Enter the same password as before, for verification.'))


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_image', 'currency_symbol', 'company_name']

        widgets = {
            'currency_symbol': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Company name')})
        }




