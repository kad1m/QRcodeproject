from django import forms
from .models import Website, CafeMenu, Category, Product, Customer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateQrCodeForm(forms.ModelForm):

    class Meta:
        model = Website
        fields = ('name',)

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': 'Your name', 'name': 'message-name'}))


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
        attrs={'class': 'form-control mb-30', 'placeholder': 'Category name', 'name': 'message-name'}))
    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': 'Description', 'name': 'message-name'}))


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'product_image')

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': 'Product name', 'name': 'message-name'}))

    price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': 'Price', 'name': 'message-name'}))

    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-30', 'placeholder': 'Description', 'name': 'message-name'}))


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'hi',
        }
    ))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'hello'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'hi',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'id': 'hi',
        }
    ))


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name']

    company_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Company name', 'id': 'hello'}))



